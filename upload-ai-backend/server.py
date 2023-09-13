import os
import uuid

from flask import Flask, request, abort
from flask_cors import CORS
from prisma import Prisma, register
from prisma.models import Video, Prompt
# from pydub import AudioSegment
from dotenv import load_dotenv
import openai

load_dotenv(override=True)

openai.api_key = os.getenv("OPEN_AI_KEY")

db = Prisma()
db.connect()
register(db)

app = Flask(__name__)

CORS(app=app, origins="*")


@app.route("/prompts")
def return_all_prompts():

    all_prompts = Prompt.prisma().find_many()

    return {"data" : [prompts.model_dump() for prompts in all_prompts]}


@app.route("/videos", methods=['POST'])
def update_video():
    # print(request.files)
    if len(request.files) == 0:
        return abort(400, description="Missing file input.")

    audio_file = request.files.get("mp4_file")

    if audio_file.filename.endswith(".mp3") == False:
        return abort(400, description="Invalid input type, please upload a MP3.")
    
    file_name = audio_file.filename[:-4]
    file_extension = audio_file.filename[-4:]
    
    if audio_file.filename == "":
        return abort(400, description="File name is empty.")
    
    new_filename = f"{file_name}-{str(uuid.uuid4())}{file_extension}"

    upload_destination = os.path.join(os.getcwd(), "tmp", new_filename)

    with open(upload_destination, 'wb') as file:
        while True:
            chunk = audio_file.read(1024)
            if not chunk:
                break
            file.write(chunk)

    video_obj = {
        "name":file_name, 
        "path":upload_destination
    }

    Video.prisma().create(data=video_obj)

    return video_obj


@app.route("/videos/<string:video_id>/transcription", methods=['POST'])
def create_transcription(video_id):
    if uuid.UUID(video_id) == False:
        return abort(400, "Invalid video_id")

    body_schema = request.get_json()

    prompt_data = body_schema.get("prompt" , "")

    if prompt_data == "":
        return abort(400, "Empty prompt")
    
    video_search = Video.prisma().find_unique_or_raise(where={"id" : video_id})

    video_data = video_search.model_dump()

    audio_file = open(video_data['path'], "rb")

    transcript = openai.Audio.transcribe(
        model="whisper-1",
        file=audio_file,
        params={
            "language" : "pt",
            "temperature" : 0,
            "prompt":prompt_data
        }
    )

    transcription = transcript['text']

    Video.prisma().update(
        where={"id" : video_id},
        data={"transcription" : transcription}
    )

    return {
        "video_id" : video_id, 
        "prompt" : prompt_data, 
        "video_path" : video_data['path'],
        "transcription_data" : transcription
    }


@app.route("/ai/complete", methods=['POST'])
def generate_ai_completion():

    body_schema = request.get_json()

    video_id = body_schema.get("video_id" , "")
    
    if uuid.UUID(video_id) == False:
        return abort(400, "Invalid video_id")
    
    template = body_schema.get("template" , "")

    temperature = body_schema.get("temperature" , 0.5)
    if temperature < 0 or temperature > 1:
        return abort(400, "Invalid temperature")
    
    video_data = Video.prisma().find_first_or_raise(where={"id" : video_id}).model_dump()

    if len(video_data["transcription"]) == 0:
        abort(400, "Video transcription was not generated yet.")
    
    prompt_message = template.replace("{transcription}", video_data["transcription"])

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        temperature=temperature,
        messages=[
            { "role" : "user", "content" : prompt_message }
        ]
    )

    return {
        "video_id" : video_id, 
        "template" : template, 
        "temperature" : temperature,
        "response" : response
    }



if __name__ == "__main__":
    app.run(debug=True)
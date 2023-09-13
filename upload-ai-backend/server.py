import os
import uuid

from flask import Flask, jsonify, session, request, abort
from prisma import Prisma, register
from prisma.models import Video, Prompt

db = Prisma()
db.connect()
register(db)

app = Flask(__name__)

@app.route("/prompts")
def return_all_prompts():

    all_prompts = Prompt.prisma().find_many()

    return {"data" : [prompts.model_dump() for prompts in all_prompts]}

@app.route("/videos", methods=['POST'])
def update_video():
    if "mp4_file" not in request.files:
        return abort(400, "Missing file input.")

    mp4_file = request.files['mp4_file']


    file_name = mp4_file.filename.split(".")[:-1]
    file_extension = mp4_file.filename.split(".")[-1]
    
    if mp4_file.filename == "":
        return abort(400, "File name is empty.")
    
    if file_extension != "mp3":
        return abort(400, "Invalid input type, please upload a MP3.")
    
    new_filename = f"{file_name}-{str(uuid.uuid4())}.{file_extension}"

    upload_destination = os.path.join(os.getcwd(), "twp", new_filename)

    mp4_file.save(upload_destination)

    print("parei no minuto 41:52 da segunda aula da nlw mastery")

    return "File uploaded successfully!"

if __name__ == "__main__":
    app.run(debug=True)
import uuid
from flask import Blueprint, request, abort, Response, stream_with_context
from prisma.models import Video
from openai_config import openai

complete_bp = Blueprint('complete', __name__)

@complete_bp.route("/ai/complete", methods=['POST'])
def generate_ai_completion():

    body_schema = request.get_json()

    print(body_schema)

    video_id = body_schema.get("video_id" , "")
    
    if uuid.UUID(video_id) == False:
        return abort(400, "Invalid video_id")
    
    prompt = body_schema.get("prompt" , "")

    temperature = body_schema.get("temperature" , 0.5)
    if temperature < 0 or temperature > 1:
        return abort(400, "Invalid temperature")
    
    video_data = Video.prisma().find_first_or_raise(where={"id" : video_id}).model_dump()

    if len(video_data["transcription"]) == 0:
        abort(400, "Video transcription was not generated yet.")
    
    prompt_message = prompt.replace("{transcription}", video_data["transcription"])

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        temperature=temperature,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        messages=[
            { "role" : "user", "content" : prompt_message }
        ],
        stream=True
    )

    def generate():
        for chunk in response:
            current_content = chunk["choices"][0]["delta"].get("content", "")
            yield current_content
    
    return Response(stream_with_context(generate()))


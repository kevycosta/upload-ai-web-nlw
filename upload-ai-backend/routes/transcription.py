import uuid
from flask import Blueprint, request, abort
from prisma.models import Video
from openai_config import openai

transcription_bp = Blueprint('transcription', __name__)

@transcription_bp.route("/videos/<string:video_id>/transcription", methods=['POST'])
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
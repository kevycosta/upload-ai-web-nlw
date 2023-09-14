import os
import uuid

from flask import Blueprint, request, abort
from prisma.models import Video

videos_bp = Blueprint('videos', __name__)


@videos_bp.route("/videos", methods=['POST'])
def update_video():
    # print(request.files)
    if len(request.files) == 0:
        return abort(400, description="Missing file input.")

    audio_file = request.files.get("file")

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

    video_obj = Video.prisma().create(data={
        "name":file_name, 
        "path":upload_destination
    })

    return video_obj.model_dump_json()

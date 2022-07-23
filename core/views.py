from fastapi import Depends, HTTPException, Response, File, UploadFile, BackgroundTasks
from videostore import db_init
from sqlalchemy.orm import Session
from core import services
from core import schema as core_schema
from fastapi import status
from . import dependencies
from starlette.responses import StreamingResponse
import string, random


async def get_videos(db_session: Session = Depends(db_init.get_db)):
    return services.get_videos_fromdb(db_session)


async def pre_post_video(
    video_schema: core_schema.VideoPydanticModel,
    db_session: Session = Depends(db_init.get_db),
):
    return services.insert_video(db_session, video_schema)


async def get_video(
    id: int,
    db_session: Session = Depends(db_init.get_db),
):
    if value := services.get_video_by_id(db_session=db_session, video_id=id):
        return value
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


async def post_video(
    background_task: BackgroundTasks,
    file: UploadFile = Depends(dependencies.FileTypeChecker()),
    db_session: Session = Depends(db_init.get_db),
):
    if services.get_video_by_url(video_url=file.filename, db_session=db_session):
        name, extension = file.filename.split(".")
        name = name + "".join(
            random.choices(string.ascii_letters + string.digits, k=10)
        )
        file.filename = f"{name}.{extension}"

    video_pydantic = core_schema.VideoPydanticModel(
        url=file.filename, status="video on queue"
    )
    video: core_schema.VideoPydanticModel = services.insert_video(
        video_schema=video_pydantic, db_session=db_session
    )
    background_task.add_task(services.write_to_disk, file=file, video_id=video.id)

    return video


def get_data_from_file(file_path: str):
    with open(file_path, "rb") as f:
        yield f.read()


async def stream_video(file_name: str):
    try:
        file_content = get_data_from_file(f"uploads/{file_name}")
        return StreamingResponse(
            content=file_content,
            media_type="video/mp4",
            status_code=status.HTTP_200_OK,
        )
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

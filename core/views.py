from fastapi import (
    Depends,
    HTTPException,
    Response,
    UploadFile,
    BackgroundTasks,
    status,
)
from videostore import db_init
from sqlalchemy.orm import Session
from . import dependencies, schema, services
from starlette.responses import StreamingResponse
import string, random


async def get_videos(
    start_length: float = None,
    end_length: float = None,
    start_size: float = None,
    end_size: float = None,
    start_date: str = None,
    end_date: str = None,
    db_session: Session = Depends(db_init.get_db),
):
    """
    Returns a list of videos from the database.
    if every parameter is None, it returns all videos.\n
    Else it returns videos that match the parameters.
    """
    return services.get_videos_fromdb(
        db_session,
        start_length=start_length,
        end_length=end_length,
        start_size=start_size,
        end_size=end_size,
        start_date=start_date,
        end_date=end_date,
    )


async def get_video(
    id: int,
    db_session: Session = Depends(db_init.get_db),
):
    """
    returns a video object in json format according to its id
    """
    if value := services.get_video_by_id(db_session=db_session, video_id=id):
        return value
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


async def post_video(
    background_task: BackgroundTasks,
    file: UploadFile = Depends(dependencies.FileTypeChecker()),
    db_session: Session = Depends(db_init.get_db),
) -> schema.VideoPydanticModel:
    """
    This controller handles the video upload.\n
        request_body: {file : video}
    returns a new video object in json format.\n
        response body: {id: int, url: str, created_at: str, status: str, remarks: str, length: float, size: float}
    """

    # check if file with same name exists in the filesystem
    if services.get_video_by_url(video_url=file.filename, db_session=db_session):
        # generate a new file name
        name, extension = file.filename.split(".")
        name = name + "".join(
            random.choices(string.ascii_letters + string.digits, k=10)
        )
        file.filename = f"{name}.{extension}"

    video_pydantic = schema.VideoPydanticModel(url=file.filename, status="on_queue")
    video: schema.VideoPydanticModel = services.insert_video(
        video_schema=video_pydantic, db_session=db_session
    )

    background_task.add_task(services.write_to_disk, file=file, video_id=video.id)
    return video


async def stream_video(file_name: str):
    try:
        file_content = services.get_data_from_file(f"uploads/{file_name}")
        return StreamingResponse(
            content=file_content,
            media_type=f"video/{file_name.split('.')[-1]}",
            status_code=status.HTTP_200_OK,
        )
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


async def calculate_payment(
    video_length: float = 1,
    video_size: float = 1,
    video_type: str = Depends(dependencies.video_type_checker),
):
    payment = {"total": 0}
    if video_size < 524_288_000:
        payment["total"] += 5
    else:
        payment["total"] += 12.5
    if video_length < 378:
        payment["total"] += 12.5
    else:
        payment["total"] += 20
    return payment

from typing import List, Generator
from fastapi import UploadFile
from sqlalchemy.orm import Session
from . import models, schema
from worker import worker_init
from sqlalchemy.dialects import postgresql


def insert_video(
    db_session: Session,
    video_schema: schema.VideoPydanticModel,
) -> schema.VideoPydanticModel:

    db_video = models.Video(
        url=video_schema.url,
        status=video_schema.status,
    )
    db_session.add(db_video)
    db_session.commit()
    db_session.refresh(db_video)
    return db_video


def get_videos_fromdb(
    db_session: Session,
    start_length: float = None,
    end_length: float = None,
    start_size: float = None,
    end_size: float = None,
    start_date: str = None,
    end_date: str = None,
) -> List[schema.VideoPydanticModel]:
    videos = db_session.query(models.Video).filter(models.Video.status == "done")
    if start_length:
        videos = videos.filter(models.Video.length >= start_length)
    if end_length:
        videos = videos.filter(models.Video.length <= end_length)
    if start_size:
        videos = videos.filter(models.Video.size >= start_size)
    if end_size:
        videos = videos.filter(models.Video.size <= end_size)
    if start_date:
        videos = videos.filter(models.Video.created_at >= start_date)
    if end_date:
        videos = videos.filter(models.Video.created_at <= end_date)
    return videos.all()


def get_video_by_id(
    video_id: int,
    db_session: Session,
) -> schema.VideoPydanticModel:
    return db_session.query(models.Video).get(video_id)


def get_video_by_url(video_url: str, db_session: Session) -> schema.VideoPydanticModel:
    return db_session.query(models.Video).filter_by(url=video_url).first()


def write_to_disk(file: UploadFile, video_id: int) -> None:
    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(file.file.read())
    worker_init.check_video_size.send(video_id=video_id)


def get_data_from_file(file_path: str) -> Generator | None:
    with open(file_path, "rb") as f:
        yield f.read()

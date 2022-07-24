from typing import List, Generator
from fastapi import UploadFile
from sqlalchemy.orm import Session
from . import models, schema
from worker import worker_init


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
    length: float = None,
    size: float = None,
    created_at: int = None,
) -> List[schema.VideoPydanticModel]:
    return (
        db_session.query(models.Video).filter_by(
            status="done",
            **{
                key: value
                for key, value in locals().items()
                if value is not None and key != "db_session"
            },
        )
    ).all()


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
    worker_init.check_size.send(video_id=video_id)


def get_data_from_file(file_path: str) -> Generator | None:
    with open(file_path, "rb") as f:
        yield f.read()

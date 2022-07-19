from sqlalchemy.orm import Session
from core import schema as core_schema
from . import models


def insert_video(
    db_session: Session,
    video_schema: core_schema.VideoPydanticModel,
):

    db_video = models.Video(
        title=video_schema.title,
        url=video_schema.url,
    )
    db_session.add(db_video)
    db_session.commit()
    db_session.refresh(db_video)
    return db_video


def get_videos_fromdb(db_session: Session):
    return db_session.query(models.Video).all()


def get_video_by_id(
    video_id: int,
    db_session: Session,
):
    return db_session.query(models.Video).get(video_id)

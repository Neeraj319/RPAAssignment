from fastapi import Depends, Response
from videostore import db_init
from sqlalchemy.orm import Session
from core import services as core_services
from core import schema as core_schema
from fastapi import status


async def get_videos(db_session: Session = Depends(db_init.get_db)):
    return core_services.get_videos_fromdb(db_session)


async def post_video(
    video_schema: core_schema.VideoPydanticModel,
    db_session: Session = Depends(db_init.get_db),
):
    return core_services.insert_video(db_session, video_schema)


async def get_video(
    id: int,
    db_session: Session = Depends(db_init.get_db),
):
    if value := core_services.get_video_by_id(db_session=db_session, video_id=id):
        return value
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

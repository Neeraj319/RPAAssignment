from fastapi import Depends
from videostore import db_init
from sqlalchemy.orm import Session
from core import services as core_severices


async def get_videos(db_session: Session = Depends(db_init.get_db)):
    return core_severices.get_videos(db_session)

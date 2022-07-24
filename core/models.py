from sqlalchemy import Column, Integer, String, DateTime, Boolean, VARCHAR
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

metadata = Base.metadata


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(VARCHAR(length=200), nullable=False, unique=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
    )
    status = Column(VARCHAR(length=200), nullable=True)

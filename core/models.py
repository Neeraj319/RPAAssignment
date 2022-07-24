from sqlalchemy import Column, Enum, Float, Integer, String, DateTime, VARCHAR
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

metadata = Base.metadata


class StatusEnum(enum.Enum):
    on_queue = "on_queue"
    processing = "processing"
    done = "done"
    canceled = "canceled"


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(VARCHAR(length=200), nullable=False, unique=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
    )
    status = Column(
        Enum(StatusEnum),
        nullable=False,
    )
    size = Column(Float, nullable=True)
    length = Column(Float, nullable=True)
    remarks = Column(String(length=100), nullable=True)

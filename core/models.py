from sqlalchemy import Column, Enum, Float, Integer, String, DateTime, VARCHAR
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from . import enums

Base = declarative_base()

metadata = Base.metadata


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(
        VARCHAR(length=200), nullable=False, unique=True
    )  # this also refers to the file name in the filesystem
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
    )
    status = Column(
        Enum(enums.StatusEnum),
        nullable=False,
    )
    size = Column(Float, nullable=True)
    length = Column(Float, nullable=True)
    remarks = Column(String(length=100), nullable=True)

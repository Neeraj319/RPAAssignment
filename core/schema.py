from typing import Optional
from pydantic import BaseModel
import datetime


class VideoPydanticModel(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    url: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True

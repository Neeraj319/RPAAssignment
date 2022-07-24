from typing import Optional
from pydantic import BaseModel
import datetime


class VideoPydanticModel(BaseModel):
    id: Optional[int] = None
    url: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    status: str
    remarks: Optional[str] = None
    length: Optional[float] = None
    size: Optional[float] = None

    class Config:
        orm_mode = True

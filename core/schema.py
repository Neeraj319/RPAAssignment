from typing import Optional
from pydantic import BaseModel


class VideoPydanticModel(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    url: Optional[str] = None
    created_at: Optional[str] = None

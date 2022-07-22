from fastapi import APIRouter
from core import schema as core_schema
from . import views


router = APIRouter(prefix="/video", tags=["Video Upload"])


router.get("/")(views.get_videos)
router.get("/{id}/", response_model=core_schema.VideoPydanticModel)(views.get_video)
router.post("/")(views.post_video)

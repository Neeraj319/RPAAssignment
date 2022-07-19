from fastapi import APIRouter
from core import schema as core_schema
from . import views


router = APIRouter(prefix="/video", tags=["Video Upload"])


router.get("/")(views.get_videos)

router.post("/", response_model=core_schema.VideoPydanticModel)(views.post_video)
router.get("/{id}/", response_model=core_schema.VideoPydanticModel)(views.get_video)

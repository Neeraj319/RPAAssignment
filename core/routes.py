from fastapi import APIRouter

from . import views


router = APIRouter(prefix="/video", tags=["Video Upload"])


router.get("/")(views.get_videos)

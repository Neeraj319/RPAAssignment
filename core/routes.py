from fastapi import APIRouter
from core import schema as core_schema
from . import views


router = APIRouter(prefix="/video", tags=["Video Upload"])


router.get("/")(views.get_videos)
router.get("/{id}/")(views.get_video)
router.post("/")(views.post_video)
router.get("/stream/{file_name}/")(views.stream_video)
router.get("/payment")(views.calculate_payment)

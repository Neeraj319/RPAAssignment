from typing import List
from fastapi import APIRouter
from core import schema
from . import views
from starlette.responses import StreamingResponse

router = APIRouter(prefix="/video", tags=["Video Upload"])


router.get("/", response_model=List[schema.VideoPydanticModel])(views.get_videos)
router.get("/{id}/", response_model=schema.VideoPydanticModel)(views.get_video)
router.post("/", response_model=schema.VideoPydanticModel)(views.post_video)
router.get("/stream/{file_name}/", response_class=StreamingResponse)(views.stream_video)
router.get("/payment")(views.calculate_payment)

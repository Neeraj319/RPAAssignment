from typing import Tuple
from fastapi import UploadFile, HTTPException, status


class FileTypeChecker:
    def __init__(
        self,
        allowed_extension_type: Tuple = ("mp4", "mkv"),
        allowed_file: str = "video",
    ) -> None:
        self.allowed_extension_type = allowed_extension_type
        self.allowed_file = allowed_file

    async def __call__(self, file: UploadFile) -> UploadFile:
        content_type = file.content_type.split("/")[0]
        file_extension = file.filename.split(".")[-1]
        if content_type != self.allowed_file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="only video allowed"
            )
        if file_extension not in self.allowed_extension_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="only mkv or mp4 files allowed",
            )
        return file


def video_type_checker(video_type: str):
    if video_type in ("mp4", "mkv"):
        return video_type
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="only mk4 or mp4 files allowed",
        )

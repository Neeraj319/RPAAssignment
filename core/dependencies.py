from typing import Tuple
from fastapi import UploadFile, HTTPException, status


class FileContentChecker:
    def __init__(
        self,
        allowed_extension_type: Tuple = ("mp4", "mkv"),
        allowed_file: str = "video",
    ) -> None:
        self.allowed_extension_type = allowed_extension_type
        self.allowed_file = allowed_file

    def __call__(self, file: UploadFile):
        content_type = file.content_type.split("/")
        if content_type[0] != self.allowed_file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="only video allowed"
            )
        if content_type[1] not in self.allowed_extension_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="only mk4 or mp4 files allowed",
            )
        return file

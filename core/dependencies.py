from typing import Tuple, Any
from fastapi import Depends, UploadFile, HTTPException, status
import subprocess


class FileTypeChecker:
    def __init__(
        self,
        allowed_extension_type: Tuple = ("mp4", "mkv"),
        allowed_file: str = "video",
    ) -> None:
        self.allowed_extension_type = allowed_extension_type
        self.allowed_file = allowed_file

    async def __call__(self, file: UploadFile):
        print("in file type checker")

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


class FileSizeChecker:
    def __call__(self, file: UploadFile = Depends(FileTypeChecker())) -> Any:
        print("in size checker")
        file_data = file.file.read()
        if len(file_data) > 1073741824:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="file size should be less than 1 gb",
            )
        return file, file_data


class VideoLengthChecker:
    def __call__(self, file: UploadFile = Depends(FileSizeChecker())):
        print("in video length checker")

        with open(file[0].filename, "wb") as out_file:
            out_file.write(file[1])
            result = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "default=noprint_wrappers=1:nokey=1",
                    file[0].filename,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            if float(result.stdout) > 600:
                subprocess.run(["rm", file.filename])
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="video cannot be of more than 10 minutes long",
                )
        return file[0]

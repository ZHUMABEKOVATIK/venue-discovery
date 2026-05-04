import os
import uuid
from fastapi import UploadFile, HTTPException
from src.core.exceptions import BadRequestException

UPLOAD_DIR = "media"
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE = 5 * 1024 * 1024  # 5MB


async def save_image(file: UploadFile, folder: str) -> str:
    if file.content_type not in ALLOWED_TYPES:
        raise BadRequestException("Fayl formatı natuwrı. Tek ǵana JPEG, PNG, WEBP formatta")

    contents = await file.read()

    if len(contents) > MAX_SIZE:
        raise HTTPException(400, "Fayl kólemi 5MB tan aspawı tiyis")

    ext = file.filename.split(".")[-1].lower()
    filename = f"{uuid.uuid4()}.{ext}"

    dir_path = os.path.join(UPLOAD_DIR, folder)
    os.makedirs(dir_path, exist_ok=True)

    filepath = os.path.join(dir_path, filename)
    with open(filepath, "wb") as f:
        f.write(contents)

    return f"/{dir_path}/{filename}"  # /media/announcements/uuid.jpg


def delete_image(url: str) -> None:
    path = url.lstrip("/")
    if os.path.exists(path):
        os.remove(path)
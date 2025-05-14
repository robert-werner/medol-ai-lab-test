import os
import shutil

from fastapi import UploadFile
from minio import Minio

from app.db.models.orm.file_info import FileInfo
from app.settings import async_session_local, settings


async def add_file(file_uuid: str, filepath: str):
    async with async_session_local() as session:
        async with session.begin():
            new_file = FileInfo(id=file_uuid,
                                uri=filepath)
            session.add(new_file)
            await session.commit()


async def save_temp_file(file: UploadFile):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return temp_path


async def upload_to_minio(file_path: str, filename: str):
    client = Minio(
        "localhost:9000",
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=False
    )

    bucket = "medol"
    client.fput_object(bucket, filename, file_path)

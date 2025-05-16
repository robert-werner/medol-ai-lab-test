from datetime import timedelta
import uuid

from fastapi import (BackgroundTasks, Depends, FastAPI, File, Form,
                     HTTPException, UploadFile)
from minio import Minio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import StreamingResponse

from app.db.models.orm.base import Base
from app.db.models.orm.file_info import FileInfo
from app.db.models.orm.user import User
from app.db.models.pydantic.token import Token
from app.db.models.pydantic.user import UserCreate, UserResponse
from app.settings import (create_access_token, engine, get_current_user,
                          get_db, pwd_context, settings)
from app.utils import add_file, save_temp_file, upload_to_minio

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await db.get(User, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@app.post("/login", response_model=Token)
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    user = await db.get(User, username)
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=UserResponse)
async def read_current_user(
    current_user: User = Depends(get_current_user)
):
    return current_user

@app.post("/upload")
async def upload(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    file_uuid = str(uuid.uuid4())
    file_path = f"{file.filename}"

    temp_path = await save_temp_file(file)

    background_tasks.add_task(upload_to_minio, temp_path, file.filename)

    await add_file(file_uuid, file_path)

    return {
        "id": file_uuid,
        "filename": file.filename,
    }

@app.get("/download/{file_uuid}")
async def download_file(file_uuid: str,
                        db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    check_file = await db.get(FileInfo, file_uuid)
    if not check_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")


    client = Minio(
        "localhost:9000",
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=False
    )

    response = client.get_object("medol", check_file.uri)

    def iter_file():
        try:
            for chunk in response.stream(32 * 1024):  # 32KB chunks
                yield chunk
        finally:
            response.close()
            response.release_conn()

    return StreamingResponse(
        content=iter_file(),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={check_file.uri.split('/')[-1]}"
        }
    )

@app.get("/files")
async def files(db: AsyncSession = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    query = await db.execute(select(FileInfo))
    result = []
    for row in query.scalars().all():
        result.append(
            {
                "id": row.id,
                "filename": row.uri
            }
        )
    return result

@app.get("/health")
def health_check():
    return {"status": "ok"}

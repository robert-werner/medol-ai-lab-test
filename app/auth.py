from fastapi import APIRouter, Form, HTTPException

from app.auth import authenticate_user
from app.core.logger import CLogger
from app.db.models.base import async_session_local
from app.schemas.responses.auth import LoginResponse

router = APIRouter(prefix='/auth')
logger = CLogger("Auth Router").get_logger()

@router.post('/login', response_model=LoginResponse)
async def login(
        username: str = Form(...),
        password: str = Form(...)
):
    async with async_session_local() as session:
        async with session.begin():
            ыу
            user = authenticate_user(session, username, password)
            if not user:
                raise HTTPException(status_code=401, detail="Invalid username or password")
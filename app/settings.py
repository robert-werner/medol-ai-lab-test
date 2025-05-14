from datetime import datetime, timedelta
from typing import Any, AsyncGenerator, Optional

from decouple import UndefinedValueError, config
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette import status

from app.db.models.orm.user import User


class Settings(object):  # noqa: WPS230
    """Class with server settings."""

    def __init__(self) -> None:
        """Create class with server settings."""
        self.db_user = self.get_setting("DB_USER", "medol")
        self.db_password = self.get_setting("DB_PASSWORD", "medol")
        self.db_name = self.get_setting("DB_NAME", "medol")
        self.db_host = self.get_setting("DB_HOST", "localhost")
        self.db_port = self.get_setting("DB_PORT", "6432")
        self.secret_key = self.get_setting("SECRET_KEY", "medol")
        self.algorithm = self.get_setting("ALGORITHM", "HS256")
        self.access_token_expire_minutes = self.get_setting(
            "ACCESS_TOKEN_EXPIRE_MINUTES", 30
        )
        self.minio_secret_key = self.get_setting("MINIO_SECRET_KEY", "promedol")
        self.minio_access_key = self.get_setting("MINIO_ACCESS_KEY", "promedol")

    def get_setting(self, name: str, default: Any) -> Any:
        """Get setting.

        :param name: Setting name
        :param default: Default value
        :return: Setting value
        """
        setting = None
        try:
            setting = config(name)
        except UndefinedValueError:
            setting = default

        return setting


settings = Settings()


DB_USER = settings.db_user
DB_PASSWORD = settings.db_password
DB_NAME = settings.db_name
DB_HOST = settings.db_host
DB_PORT = settings.db_port


def get_db_string(
    host: str = DB_HOST,
    port: str = DB_PORT,
    database: str = DB_NAME,
    user: str = DB_USER,
    password: str = DB_PASSWORD,
):
    """Get database connection string.

    :param host: Database address
    :param port: Database port
    :param database: Database name
    :param user: Username
    :param password: User password
    :return: Connection string
    """
    credentials = f"{user}:{password}"
    address = f"{host}:{port}/{database}"
    return "".join(["postgresql+asyncpg://", credentials, "@", address])


security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
engine = create_async_engine(get_db_string(), echo=True)
async_session_local = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


async def get_db() -> AsyncGenerator[Any, Any]:
    async with async_session_local() as session:
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.get(User, username)
    if user is None:
        raise credentials_exception
    return user

from collections import namedtuple
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated, Any, Optional

import jwt
from fastapi import Cookie, Depends, HTTPException

from app.settings import settings

VerifiedJwtData = namedtuple("VerifiedJwtData", ["user_id", "access_token"])


class JWTManager:
    @staticmethod
    def create_token(
        data: dict, expires_delta: Optional[timedelta], minutes: int
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now() + (
            expires_delta if expires_delta else timedelta(minutes=minutes)
        )
        to_encode["exp"] = expire.timestamp()
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    @staticmethod
    def create_access_token(
        data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        return JWTManager.create_token(data, expires_delta, 15)

    @staticmethod
    def create_refresh_token(
        data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        return JWTManager.create_token(data, expires_delta, 120)

    @staticmethod
    def decode_token(token: str) -> Any | None:
        try:
            return jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        except jwt.exceptions.ExpiredSignatureError:
            return None
        except jwt.exceptions.InvalidTokenError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail={"data": "Invalid JWT token"},
            )

    @staticmethod
    def verify_token(
        access_token: Annotated[str | None, Cookie()] = None,
        refresh_token: Annotated[str | None, Cookie()] = None,
    ) -> VerifiedJwtData | HTTPException:
        if not access_token and not refresh_token:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail={"data": "No token provided"},
            )

        decoded_token = JWTManager.decode_token(access_token) if access_token else None
        new_access_token = None

        if not decoded_token and refresh_token:
            data = JWTManager.decode_token(refresh_token)
            if not data or "exp" not in data or "sub_refresh" not in data:
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid refresh token"
                )
            new_access_token = JWTManager.create_access_token(
                data={"sub": data["sub_refresh"]},
                expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
            )
            user_id = int(data.get("sub_refresh", -1))
        elif decoded_token:
            user_id = int(decoded_token.get("sub", -1))
        else:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail={"data": "Invalid JWT token"},
            )

        if user_id <= 0:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail={"data": "Invalid JWT token"},
            )
        return VerifiedJwtData(user_id=user_id, access_token=new_access_token)


JWT_verify = Annotated[VerifiedJwtData, Depends(JWTManager.verify_token)]

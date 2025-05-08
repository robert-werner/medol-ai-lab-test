"""Middleware для обработки аутентификации."""

import traceback
from datetime import datetime, timezone

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.logger import logger
from app.exceptions.domain import InvalidTokenError
from app.utils.jwt import JWTManager


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.public_paths = {
            "/api/v1/auth/login",
            "/api/v1/auth/dev_login",
            "/docs",
            "/openapi.json",
            "/oauth2-redirect",
        }

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.public_paths:
            return await call_next(request)

        try:
            # Получаем Bearer токен из заголовка
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Отсутствует заголовок авторизации"},
                )

            if not auth_header.startswith("Bearer "):
                detail = "Неверный формат токена. Ожидается: Bearer <token>"
                return JSONResponse(status_code=401, content={"detail": detail})

            token = auth_header.split(" ")[1]

            try:
                # Проверяем токен
                payload = JWTManager.decode_token(token)

                # Проверяем срок действия
                exp = datetime.fromtimestamp(payload["exp"])
                current_time = datetime.now(timezone.utc)
                if exp < current_time:
                    logger.warning(
                        "Token expired",
                        extra={
                            "token_exp": exp.isoformat(),
                            "current_time": current_time.isoformat(),
                        },
                    )
                    raise InvalidTokenError("Срок действия токена истек")

                # Добавляем user_id в request state
                request.state.user_id = int(payload["sub"])
                return await call_next(request)

            except InvalidTokenError as e:
                logger.warning(
                    "Invalid token", extra={"error": str(e), "path": request.url.path}
                )
                return JSONResponse(status_code=401, content={"detail": str(e)})

        except Exception as e:
            logger.error(
                "Auth middleware error",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "path": request.url.path,
                    "traceback": traceback.format_exc(),
                },
            )
            return JSONResponse(
                status_code=500, content={"detail": "Внутренняя ошибка сервера"}
            )

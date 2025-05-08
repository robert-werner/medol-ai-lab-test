from http import HTTPStatus

from app.exceptions.generic import GenericException


class ResourceNotFoundError(GenericException):
    """Базовый класс для всех ошибок отсутствия ресурса."""

    http_status = HTTPStatus.NOT_FOUND


class UserNotFoundError(ResourceNotFoundError):
    """Возникает, когда пользователь не найден в системе."""

    def __init__(self, user_id: int):
        super().__init__(f"Пользователь с ID {user_id} не найден")


class AccountNotFoundError(ResourceNotFoundError):
    """Возникает, когда счет не найден в системе."""

    def __init__(self, account_id: str):
        super().__init__(f"Счет {account_id} не найден")


class ValidationError(GenericException):
    """Базовый класс для всех ошибок валидации."""

    http_status = HTTPStatus.BAD_REQUEST

class AuthenticationError(GenericException):
    """Базовый класс для всех ошибок аутентификации."""

    http_status = HTTPStatus.UNAUTHORIZED


class AuthorizationError(GenericException):
    """Базовый класс для всех ошибок авторизации."""

    http_status = HTTPStatus.FORBIDDEN

class InvalidTokenError(AuthenticationError):
    """Возникает при недействительном токене."""

    def __init__(self, message: str = "Недействительный токен"):
        super().__init__(message)

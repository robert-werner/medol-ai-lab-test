from pydantic import BaseModel

from typing import Optional


class UserAuthRequest(BaseModel):
    init_data: str


class UpdateUserRequest(BaseModel):
    user_name: Optional[str] = None


class UpdateAccessTokenRequest(BaseModel):
    refresh_token: str


class UpdateUserStateRequest(BaseModel):
    last_active_resource: Optional[str] = None
    last_opened_page: Optional[str] = None

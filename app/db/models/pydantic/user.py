from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserInDB(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str

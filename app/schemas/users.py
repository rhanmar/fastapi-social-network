from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    """Схема Пользователя."""

    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


class UserListSchema(BaseModel):
    """Схема списка Пользователей."""

    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserRegisterSchema(BaseModel):
    """Схема регистрации Пользователя."""

    username: str
    email: str
    password: str


class UserLoginSchema(BaseModel):
    """Схема логина Пользователя."""

    username: str
    password: str

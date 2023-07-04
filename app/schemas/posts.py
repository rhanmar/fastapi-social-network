from datetime import datetime

from pydantic import BaseModel

from app.schemas import UserInPost


class PostListSchema(BaseModel):
    """Схема Списка Публикаций."""

    id: int
    text: str
    created_at: datetime
    likes_count: int
    dislikes_count: int
    user: UserInPost

    class Config:
        orm_mode = True


class PostDetailSchema(BaseModel):
    """Схема Публикации."""

    id: int
    text: str
    created_at: datetime
    likes_count: int
    dislikes_count: int
    user: UserInPost

    class Config:
        orm_mode = True


class PostCreateSchema(BaseModel):
    """Схема создания Публикации."""

    text: str

    class Config:
        orm_mode = True


class PostEditSchema(BaseModel):
    """Схема изменения Публикации."""

    text: str

    class Config:
        orm_mode = True

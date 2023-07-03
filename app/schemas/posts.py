from datetime import datetime

from pydantic import BaseModel


class PostListSchema(BaseModel):
    """Схема Списка Публикаций."""

    id: int
    text: str
    created_at: datetime
    likes_count: int
    dislikes_count: int

    class Config:
        orm_mode = True


class PostDetailSchema(BaseModel):
    """Схема Публикации."""

    id: int
    text: str
    created_at: datetime
    likes_count: int
    dislikes_count: int

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

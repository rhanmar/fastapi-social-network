from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models import Post, User
from app.routers.users import get_current_user
from app.schemas import PostCreateSchema, PostDetailSchema, PostEditSchema, PostListSchema
from app.services import PostService

router = APIRouter(
    prefix="/api/posts",
)


def get_post_service(db: Session = Depends(get_db)) -> PostService:
    """Получить объект сервиса для работы с Публикациями."""
    return PostService(db=db)


@router.get("/mine/", response_model=list[PostListSchema])
def my_posts(
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
) -> list[Post]:
    """Публикации авторизированного Пользователя."""
    return post_service.get_posts_for_user(current_user)


@router.get("/", response_model=list[PostListSchema])
def posts_list(post_service: PostService = Depends(get_post_service)) -> list[Post]:
    """Список всех Публикаций."""
    return post_service.get_all_posts()


@router.get("/{post_id}/", response_model=PostDetailSchema)
def posts_detail(post_id: int, post_service: PostService = Depends(get_post_service)) -> Post:
    """Детальная информация о Публикации."""
    return post_service.get_post_by_params(id=post_id)


@router.post("/")
def posts_create(
    post: PostCreateSchema,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
) -> dict:
    """Создать Публикацию."""
    return post_service.create_post(post, current_user)


@router.patch("/{post_id}/")
def posts_edit(
    post_id: int,
    post: PostEditSchema,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
) -> dict:
    """Изменить Публикацию."""
    return post_service.edit_post(post_id, post, current_user)


@router.delete("/{post_id}/")
def posts_delete(
    post_id: int,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
) -> dict:
    """Удалить Публикацию."""
    return post_service.delete_post(post_id, current_user)


@router.post("/{post_id}/like/")
def posts_like(
    post_id: int,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
) -> dict:
    """Поставить лайк Публикации."""
    return post_service.like_post(post_id, current_user)


@router.post("/{post_id}/dislike/")
def posts_dislike(
    post_id: int,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
) -> dict:
    """Поставить дизлайк Публикации."""
    return post_service.dislike_post(post_id, current_user)

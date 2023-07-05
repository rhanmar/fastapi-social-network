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


@router.get("/mine/", response_model=list[PostListSchema])
def my_posts(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> list[Post]:
    """Публикации Пользователя."""
    posts_service = PostService()
    return posts_service.get_posts_for_user(current_user, db)


@router.get("/", response_model=list[PostListSchema])
def posts_list(db: Session = Depends(get_db)) -> list[Post]:
    """Список Публикаций."""
    posts_service = PostService()
    return posts_service.get_all_posts(db)


@router.get("/{post_id}/", response_model=PostDetailSchema)
def posts_detail(post_id: int, db: Session = Depends(get_db)) -> Post:
    """Детальная информация о Публикации."""
    posts_service = PostService()
    return posts_service.get_post_by_params(db, id=post_id)


@router.post("/")
def posts_create(
    post: PostCreateSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Создать Публикацию."""
    posts_service = PostService()
    return posts_service.create_post(post, current_user, db)


@router.patch("/{post_id}/")
def posts_edit(
    post_id: int,
    post: PostEditSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Изменить Публикацию."""
    posts_service = PostService()
    return posts_service.edit_post(post_id, post, current_user, db)


@router.delete("/{post_id}/")
def posts_delete(
    post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    """Удалить Публикацию."""
    posts_service = PostService()
    return posts_service.delete_post(post_id, current_user, db)


@router.post("/{post_id}/like/")
def posts_like(
    post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    """Поставить лайк Публикации."""
    posts_service = PostService()
    return posts_service.like_post(post_id, current_user, db)


@router.post("/{post_id}/dislike/")
def posts_dislike(
    post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    """Поставить дизлайк Публикации."""
    posts_service = PostService()
    return posts_service.dislike_post(post_id, current_user, db)

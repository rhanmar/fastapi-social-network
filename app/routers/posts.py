from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models import Post, User
from app.schemas import PostCreateSchema, PostDetailSchema, PostEditSchema, PostListSchema
from app.services import UserService

router = APIRouter(
    prefix="/api/posts",
)


@router.get("/mine/", response_model=list[PostListSchema])
def my_posts(token: str = Header(), db: Session = Depends(get_db)) -> list[Post]:
    """Публикации Пользователя."""
    service = UserService()
    user = service.get_login_user(token, db)
    posts = db.query(Post).filter_by(user_id=user.id).join(User, Post.user_id == User.id).all()
    return posts


@router.get("/", response_model=list[PostListSchema])
def posts_list(db: Session = Depends(get_db)) -> list[Post]:
    """Список Публикаций."""
    return db.query(Post).join(User, Post.user_id == User.id).all()


@router.get("/{post_id}/", response_model=PostDetailSchema)
def posts_detail(post_id: int, db: Session = Depends(get_db)) -> Post:
    """Детальная информация о Публикации."""
    post_db = db.query(Post).filter_by(id=post_id).join(User, Post.user_id == User.id).first()
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Публикация с ID {post_id} не найдена.",
        )
    return post_db


@router.post("/")
def posts_create(
    post: PostCreateSchema, token: str = Header(), db: Session = Depends(get_db)
) -> dict:
    """Создать Публикацию."""
    user_service = UserService()
    user = user_service.get_login_user(token, db)

    post = Post(text=post.text, user=user)
    db.add(post)
    db.commit()
    return {"status": status.HTTP_200_OK, "info": f"Создана публикация {post.id}"}


@router.patch("/{post_id}/")
def posts_edit(
    post_id: int, post: PostEditSchema, token: str = Header(), db: Session = Depends(get_db)
) -> dict:
    """Изменить Публикацию."""
    user_service = UserService()
    user = user_service.get_login_user(token, db)

    post_db = db.query(Post).filter_by(id=post_id, user_id=user.id).first()
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Публикация с ID {post_id} не найдена.",
        )
    post_db.text = post.text
    db.add(post_db)
    db.commit()
    return {"status": status.HTTP_200_OK, "info": f"Публикация {post_id} изменена"}


@router.delete("/{post_id}/")
def posts_delete(post_id: int, token: str = Header(), db: Session = Depends(get_db)) -> dict:
    """Удалить Публикацию."""
    user_service = UserService()
    user = user_service.get_login_user(token, db)

    post_db = db.query(Post).filter_by(id=post_id, user_id=user.id).first()
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Публикация с ID {post_id} не найдена.",
        )
    db.delete(post_db)
    db.commit()
    return {
        "status": status.HTTP_204_NO_CONTENT,
        "info": f"Публикация {post_id} удалена",
    }


@router.post("/{post_id}/like/")
def posts_like(post_id: int, token: str = Header(), db: Session = Depends(get_db)) -> dict:
    """Поставить лайк Публикации."""
    user_service = UserService()
    user = user_service.get_login_user(token, db)

    post_db = db.query(Post).filter_by(id=post_id).first()
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Публикация с ID {post_id} не найдена.",
        )
    if post_db.user_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Нельзя поставить лайк своей публикации.",
        )
    post_db.likes_count += 1
    db.add(post_db)
    db.commit()
    return {
        "status": status.HTTP_200_OK,
        "info": f"Публикации {post_id} поставлен лайк",
    }


@router.post("/{post_id}/dislike/")
def posts_dislike(post_id: int, token: str = Header(), db: Session = Depends(get_db)) -> dict:
    """Поставить дизлайк Публикации."""
    user_service = UserService()
    user = user_service.get_login_user(token, db)

    post_db = db.query(Post).filter_by(id=post_id).first()
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Публикация с ID {post_id} не найдена.",
        )
    if post_db.user_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Нельзя поставить дизлайк своей публикации.",
        )
    post_db.dislikes_count += 1
    db.add(post_db)
    db.commit()
    return {
        "status": status.HTTP_200_OK,
        "info": f"Публикации {post_id} поставлен дизлайк",
    }

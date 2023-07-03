from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models import Post
from app.schemas import PostCreateSchema, PostDetailSchema, PostEditSchema, PostListSchema

router = APIRouter(
    prefix="/api/posts",
)


@router.get("/", response_model=list[PostListSchema])
def posts_list(db: Session = Depends(get_db)) -> list[Post]:
    """Список Публикаций."""
    return db.query(Post).all()


@router.get("/{post_id}/", response_model=PostDetailSchema)
def posts_detail(post_id: int, db: Session = Depends(get_db)) -> Post:
    """Детальная информация о Публикации."""
    post_db = db.query(Post).filter_by(id=post_id).first()
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Публикация с ID {post_id} не найдена.",
        )
    return post_db


@router.post("/")
def posts_create(post: PostCreateSchema, db: Session = Depends(get_db)) -> dict:
    """Создать Публикацию."""
    post = Post(text=post.text)
    db.add(post)
    db.commit()
    return {"status": status.HTTP_200_OK, "info": f"Создана публикация {post.id}"}


@router.patch("/{post_id}/")
def posts_edit(post_id: int, post: PostEditSchema, db: Session = Depends(get_db)) -> dict:
    """Изменить Публикацию."""
    post_db = db.query(Post).filter_by(id=post_id).first()
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
def posts_delete(post_id: int, db: Session = Depends(get_db)) -> dict:
    """Удалить Публикацию."""
    post_db = db.query(Post).filter_by(id=post_id).first()
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
def posts_like(post_id: int, db: Session = Depends(get_db)) -> dict:
    """Поставить лайк Публикации."""
    post_db = db.query(Post).filter_by(id=post_id).first()
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Публикация с ID {post_id} не найдена.",
        )
    post_db.likes_count += 1
    db.add(post_db)
    db.commit()
    return {
        "status": status.HTTP_200_OK,
        "info": f"Публикации {post_id} поставлен лайк",
    }


@router.post("/{post_id}/dislike/")
def posts_dislike(post_id: int, db: Session = Depends(get_db)) -> dict:
    """Поставить дизлайк Публикации."""
    post_db = db.query(Post).filter_by(id=post_id).first()
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Публикация с ID {post_id} не найдена.",
        )
    post_db.dislikes_count += 1
    db.add(post_db)
    db.commit()
    return {
        "status": status.HTTP_200_OK,
        "info": f"Публикации {post_id} поставлен дизлайк",
    }

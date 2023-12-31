from fastapi import HTTPException, status

from app.models import Post, User
from app.schemas import PostCreateSchema, PostEditSchema
from app.services import AppService


class PostService(AppService):
    """Сервис для работы с Публикацями."""

    def get_all_posts(self) -> list[Post]:
        """Получить все Публикации."""
        return self.db.query(Post).join(User, Post.user_id == User.id).all()

    def get_posts_for_user(self, user: User) -> list[Post]:
        """Получить все Публикации для указанного Пользователя."""
        return (
            self.db.query(Post).filter_by(user_id=user.id).join(User, Post.user_id == User.id).all()
        )

    def get_post_by_params(self, **kwargs) -> Post:
        """Получить Публикацию по параметрам."""
        post_db = (
            self.db.query(Post).filter_by(**kwargs).join(User, Post.user_id == User.id).first()
        )
        if not post_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Публикация не найдена.",
            )
        return post_db

    def create_post(self, post: PostCreateSchema, user: User) -> dict:
        """Создать Публикацию."""
        post = Post(text=post.text, user=user)
        self.db.add(post)
        self.db.commit()
        return {"status": status.HTTP_200_OK, "info": f"Создана публикация {post.id}"}

    def edit_post(self, post_id: int, post: PostEditSchema, user: User) -> dict:
        """Изменить Публикацию."""
        post_db = self.get_post_by_params(id=post_id, user_id=user.id)
        post_db.text = post.text
        self.db.add(post_db)
        self.db.commit()
        return {"status": status.HTTP_200_OK, "info": f"Публикация {post_id} изменена"}

    def delete_post(self, post_id: int, user: User) -> dict:
        """Удалить Публикацию."""
        post_db = self.get_post_by_params(id=post_id, user_id=user.id)
        self.db.delete(post_db)
        self.db.commit()
        return {
            "status": status.HTTP_204_NO_CONTENT,
            "info": f"Публикация {post_id} удалена",
        }

    def like_post(self, post_id: int, user: User) -> dict:
        """Поставить Публикации лайк."""
        post_db = self.get_post_by_params(id=post_id)
        if post_db.user_id == user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Нельзя поставить лайк своей публикации.",
            )
        post_db.likes_count += 1
        self.db.add(post_db)
        self.db.commit()
        return {
            "status": status.HTTP_200_OK,
            "info": f"Публикации {post_id} поставлен лайк",
        }

    def dislike_post(self, post_id: int, user: User) -> dict:
        """Поставить Публикации дизлайк."""
        post_db = self.get_post_by_params(id=post_id)
        if post_db.user_id == user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Нельзя поставить дизлайк своей публикации.",
            )
        post_db.dislikes_count += 1
        self.db.add(post_db)
        self.db.commit()
        return {
            "status": status.HTTP_200_OK,
            "info": f"Публикации {post_id} поставлен дизлайк",
        }

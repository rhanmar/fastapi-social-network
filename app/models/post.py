from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.config.database import Base


class Post(Base):
    """Публикации."""

    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")
    text = Column(Text, info={"verbose_name": "Текст публикации"})
    created_at = Column(DateTime, default=datetime.now)
    likes_count = Column(Integer, default=0, info={"verbose_name": "Количество лайков"})
    dislikes_count = Column(Integer, default=0, info={"verbose_name": "Количество дизлайков"})

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.config.database import Base


class User(Base):
    """Пользователи."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, info={"verbose_name": "Никнейм"})
    email = Column(String, info={"verbose_name": "Электронная почта"})
    # password = ...
    created_at = Column(DateTime, default=datetime.now)

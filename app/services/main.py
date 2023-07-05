from sqlalchemy.orm import Session


class DBSessionContext(object):
    """Миксин с сессией."""

    def __init__(self, db: Session):
        self.db = db


class AppService(DBSessionContext):
    """Базовый миксин сервисов."""

    ...

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models import User
from app.schemas import UserListSchema, UserLoginSchema, UserRegisterSchema, UserSchema
from app.services import UserService

router = APIRouter(
    prefix="/api/users",
)


@router.get("/", response_model=list[UserListSchema])
def users_list(db: Session = Depends(get_db)) -> list[User]:
    """Список Пользователей."""
    service = UserService()
    return service.get_all_users(db)


@router.get("/{user_id}", response_model=UserSchema)
def user_detail(user_id: int, db: Session = Depends(get_db)) -> User:
    """Список Пользователей."""
    service = UserService()
    return service.get_user_by_id(user_id, db)


@router.post("/register/")
def create_user(user: UserRegisterSchema, db: Session = Depends(get_db)) -> dict:
    """Регистрация."""
    service = UserService()
    return service.create_user(user, db)


@router.post("/login/")
def login(user: UserLoginSchema, db: Session = Depends(get_db)) -> dict:
    """Логин / получение токена."""
    service = UserService()
    return service.login(user, db)


@router.get("/me/", response_model=UserSchema)
def my_profile(token: str = Header(), db: Session = Depends(get_db)) -> User:
    """Профиль Пользователя."""
    service = UserService()
    return service.get_login_user(token, db)

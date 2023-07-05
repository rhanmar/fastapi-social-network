from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models import User
from app.schemas import UserListSchema, UserLoginSchema, UserRegisterSchema, UserSchema
from app.services import UserService

router = APIRouter(
    prefix="/api/users",
)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Получить объект сервиса для работы с Пользователями."""
    return UserService(db=db)


def get_current_user(
    token: str = Header(), user_service: UserService = Depends(get_user_service)
) -> User:
    """Получить текущего Пользователя из JWT."""
    return user_service.get_login_user(token)


@router.get("/", response_model=list[UserListSchema])
def users_list(user_service: UserService = Depends(get_user_service)) -> list[User]:
    """Список Пользователей."""
    return user_service.get_all_users()


@router.get("/{user_id}", response_model=UserSchema)
def user_detail(user_id: int, user_service: UserService = Depends(get_user_service)) -> User:
    """Детальная информация о Пользователе."""
    return user_service.get_user_by_id(user_id)


@router.post("/register/")
def create_user(
    user: UserRegisterSchema, user_service: UserService = Depends(get_user_service)
) -> dict:
    """Регистрация."""
    return user_service.create_user(user)


@router.post("/login/")
def login(user: UserLoginSchema, user_service: UserService = Depends(get_user_service)) -> dict:
    """Логин / получение токена."""
    return user_service.login(user)


@router.get("/me/", response_model=UserSchema)
def my_profile(current_user: User = Depends(get_current_user)) -> User:
    """Профиль Пользователя."""
    return current_user

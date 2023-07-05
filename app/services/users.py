from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.models import User
from app.schemas import UserLoginSchema, UserRegisterSchema
from app.services import AppService


class UserService(AppService):
    """Сервис для работы с Пользователями."""

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Верификация пароля."""
        return self.pwd_context.verify(plain_password, hashed_password)

    def _get_password_hash(self, password: str) -> str:
        """Получить хэш пароля."""
        return self.pwd_context.hash(password)

    def _get_user(self, username: str) -> User | None:
        """Получить Пользователя по никнейму."""
        user = self.db.query(User).filter_by(username=username).first()
        if user:
            return user
        return None

    def _authenticate_user(self, username: str, password: str) -> User | bool:
        """Аутентификация Пользователя по никнейму и паролю."""
        user = self._get_user(username)
        if not user:
            return False
        if not self._verify_password(password, user.hashed_password):
            return False
        return user

    def _create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        """Создать JWT."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def login(self, user: UserLoginSchema) -> dict:
        """Логин / получение токена."""
        user = self._authenticate_user(user.username, user.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self._create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def get_login_user(self, token: str) -> User:
        """Получить Пользователя из JWT."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = self._get_user(username=username)
        if user is None:
            raise credentials_exception
        return user

    def create_user(self, user: UserRegisterSchema) -> dict:
        """Создать Пользователя."""
        user_db = self.db.query(User).filter_by(username=user.username).first()
        if user_db:
            return {"status": status.HTTP_400_BAD_REQUEST, "info": "Пользователь уже существует"}
        else:
            user_db = User(
                username=user.username,
                email=user.email,
                hashed_password=self._get_password_hash(user.password),
            )
            self.db.add(user_db)
            self.db.commit()
            return {
                "status": status.HTTP_201_CREATED,
                "info": f"Создан пользователь {user_db.id} {user_db.username}",
            }

    def get_all_users(self) -> list[User]:
        """Получить всех Пользователей из БД."""
        return self.db.query(User).all()

    def get_user_by_id(self, user_id) -> User | dict:
        user = self.db.query(User).filter_by(id=user_id).first()
        if user:
            return user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с ID {user_id} не найден",
        )

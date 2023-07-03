from fastapi import APIRouter

router = APIRouter(
    prefix="/api/users",
)


@router.get("/")
def users_list() -> dict:
    """Список Пользователей."""
    return {1: "user1", 2: "user2"}

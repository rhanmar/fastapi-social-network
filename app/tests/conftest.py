import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def client():
    yield TestClient(app)


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def url_users_list():
    return "/api/users/"


@pytest.fixture()
def url_users_detail():
    return "/api/users/{}/"


@pytest.fixture()
def url_posts_list():
    return "/api/posts/"


@pytest.fixture()
def url_posts_detail():
    return "/api/posts/{}/"


@pytest.fixture()
def url_users_register():
    return "/api/users/register/"


@pytest.fixture()
def url_users_login():
    return "/api/users/login/"


@pytest.fixture()
def url_users_my_profile():
    return "/api/users/me/"

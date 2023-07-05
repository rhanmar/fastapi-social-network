import pytest
from fastapi import status

from app.models import User

from .factories import user_factory


@pytest.mark.users
class TestUsers:
    """Тесты Пользователей."""

    def test_list_users(self, test_db, client, db_session, url_users_list):
        users = [user_factory(db_session).create() for _ in range(5)]
        db_session.commit()
        assert db_session.query(User).count() == len(users)

        response = client.get(url_users_list)
        assert response.status_code == status.HTTP_200_OK
        res_json = response.json()
        assert len(res_json) == len(users)
        for user_json in res_json:
            assert "id" in user_json
            assert "username" in user_json
            assert "email" in user_json
            assert "created_at" in user_json

    def test_detail_users(self, test_db, client, db_session, url_users_detail):
        user = user_factory(db_session).create()
        db_session.commit()
        assert db_session.query(User).count() == 1

        response = client.get(url_users_detail.format(user.id))
        assert response.status_code == status.HTTP_200_OK
        user_json = response.json()
        assert "id" in user_json
        assert "username" in user_json
        assert "email" in user_json

    def test_detail_users_404(self, test_db, client, db_session, url_users_detail):
        user_id = 404
        response = client.get(url_users_detail.format(user_id))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        user_json = response.json()
        assert user_json == {"detail": f"Пользователь с ID {user_id} не найден"}

    def test_create_user(self, test_db, client, db_session, url_users_register):
        assert db_session.query(User).count() == 0
        password = "password1"
        data = {
            "username": "name1",
            "email": "email1",
            "password": password,
        }
        response = client.post(url_users_register, json=data)
        assert response.status_code == status.HTTP_200_OK

        assert db_session.query(User).count() == 1
        user_db = db_session.query(User).first()
        assert user_db.username == data["username"]
        assert user_db.email == data["email"]
        assert user_db.hashed_password != password

        res_json = response.json()
        assert res_json == {
            "status": status.HTTP_201_CREATED,
            "info": f"Создан пользователь {user_db.id} {user_db.username}",
        }

    def test_create_user_already_exists(self, test_db, client, db_session, url_users_register):
        assert db_session.query(User).count() == 0
        password = "password1"
        data = {
            "username": "name1",
            "email": "email1",
            "password": password,
        }
        response = client.post(url_users_register, json=data)
        assert response.status_code == status.HTTP_200_OK
        assert db_session.query(User).count() == 1

        response = client.post(url_users_register, json=data)
        assert response.status_code == status.HTTP_200_OK
        assert db_session.query(User).count() == 1
        res_json = response.json()
        assert res_json == {
            "status": status.HTTP_400_BAD_REQUEST,
            "info": f"Пользователь уже существует",
        }

    def test_login(self, test_db, client, db_session, url_users_register, url_users_login):
        assert db_session.query(User).count() == 0
        password = "password1"
        data_register = {
            "username": "name1",
            "email": "email1",
            "password": password,
        }
        response = client.post(url_users_register, json=data_register)
        assert response.status_code == status.HTTP_200_OK
        assert db_session.query(User).count() == 1

        data_login = {
            "username": "name1",
            "password": password,
        }
        response = client.post(url_users_login, json=data_login)
        assert response.status_code == status.HTTP_200_OK
        res_json = response.json()
        assert "access_token" in res_json
        assert "token_type" in res_json
        assert res_json["token_type"] == "bearer"

    def test_login_error(self, test_db, client, db_session, url_users_register, url_users_login):
        assert db_session.query(User).count() == 0
        password = "password1"
        wrong_password = "password123"
        data_register = {
            "username": "name1",
            "email": "email1",
            "password": password,
        }
        response = client.post(url_users_register, json=data_register)
        assert response.status_code == status.HTTP_200_OK
        assert db_session.query(User).count() == 1

        data_login = {
            "username": "name1",
            "password": wrong_password,
        }
        response = client.post(url_users_login, json=data_login)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        res_json = response.json()
        assert "detail" in res_json
        assert res_json["detail"] == "Incorrect username or password"

    def test_my_profile(
        self, test_db, client, db_session, url_users_register, url_users_login, url_users_my_profile
    ):
        assert db_session.query(User).count() == 0
        password = "password1"
        data_register = {
            "username": "name1",
            "email": "email1",
            "password": password,
        }
        response = client.post(url_users_register, json=data_register)
        assert response.status_code == status.HTTP_200_OK
        assert db_session.query(User).count() == 1

        data_login = {
            "username": "name1",
            "password": password,
        }
        response = client.post(url_users_login, json=data_login)
        assert response.status_code == status.HTTP_200_OK
        res_json = response.json()
        assert "access_token" in res_json
        assert "token_type" in res_json
        assert res_json["token_type"] == "bearer"

        token = res_json["access_token"]
        response = client.get(url_users_my_profile, headers={"token": token})
        assert response.status_code == status.HTTP_200_OK
        res_json = response.json()
        assert "id" in res_json
        assert "username" in res_json
        assert "email" in res_json

        user_db = db_session.query(User).first()
        assert user_db.id == res_json["id"]
        assert user_db.username == res_json["username"]
        assert user_db.email == res_json["email"]

    def test_my_profile_error(
        self, test_db, client, db_session, url_users_register, url_users_login, url_users_my_profile
    ):
        assert db_session.query(User).count() == 0
        password = "password1"
        data_register = {
            "username": "name1",
            "email": "email1",
            "password": password,
        }
        response = client.post(url_users_register, json=data_register)
        assert response.status_code == status.HTTP_200_OK
        assert db_session.query(User).count() == 1

        data_login = {
            "username": "name1",
            "password": password,
        }
        response = client.post(url_users_login, json=data_login)
        assert response.status_code == status.HTTP_200_OK
        res_json = response.json()
        assert "access_token" in res_json
        assert "token_type" in res_json
        assert res_json["token_type"] == "bearer"

        wrong_token = "123"
        response = client.get(url_users_my_profile, headers={"token": wrong_token})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        res_json = response.json()
        assert "detail" in res_json
        assert res_json["detail"] == "Could not validate credentials"

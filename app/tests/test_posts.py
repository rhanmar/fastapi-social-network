import pytest
from fastapi import status

from app.models import Post, User

from .factories import post_factory


@pytest.mark.posts
class TestPosts:
    """Тесты Публикаций."""

    def test_list(self, test_db, client, db_session, url_posts_list):
        posts = [post_factory(db_session).create() for _ in range(5)]
        db_session.commit()
        assert db_session.query(Post).count() == len(posts)
        assert db_session.query(User).count() == len(posts)

        response = client.get(url_posts_list)
        assert response.status_code == status.HTTP_200_OK
        res_json = response.json()
        assert len(res_json) == len(posts)
        for post_json in res_json:
            assert "id" in post_json
            assert "text" in post_json
            assert "created_at" in post_json
            assert "likes_count" in post_json
            assert "dislikes_count" in post_json
            assert "user" in post_json
            user_json = post_json["user"]
            assert "id" in user_json
            assert "username" in user_json
            assert "email" in user_json

    def test_detail(self, test_db, client, db_session, url_posts_detail):
        post = post_factory(db_session).create()
        db_session.commit()

        response = client.get(url_posts_detail.format(post.id))
        assert response.status_code == status.HTTP_200_OK
        post_json = response.json()
        assert "id" in post_json
        assert "text" in post_json
        assert "created_at" in post_json
        assert "likes_count" in post_json
        assert "dislikes_count" in post_json
        assert "user" in post_json
        user_json = post_json["user"]
        assert "id" in user_json
        assert "username" in user_json
        assert "email" in user_json

    def test_detail_404(self, test_db, client, db_session, url_posts_detail):
        post_id = 404
        response = client.get(url_posts_detail.format(post_id))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_my_posts(
        self,
        test_db,
        client,
        db_session,
        url_posts_detail,
        url_users_register,
        url_users_login,
        url_users_my_posts,
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

        user_db = db_session.query(User).first()
        posts = [post_factory(db_session).create(user=user_db) for _ in range(5)]
        db_session.commit()
        assert db_session.query(Post).count() == len(posts)

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

        response = client.get(url_users_my_posts, headers={"token": token})
        assert response.status_code == status.HTTP_200_OK
        res_json = response.json()
        assert len(res_json) == len(posts)
        for post_json in res_json:
            assert "id" in post_json
            assert "text" in post_json
            assert "created_at" in post_json
            assert "likes_count" in post_json
            assert "dislikes_count" in post_json
            assert "user" in post_json
            user_json = post_json["user"]
            assert "id" in user_json
            assert "username" in user_json
            assert "email" in user_json

    def test_create(
        self, test_db, client, db_session, url_posts_list, url_users_register, url_users_login
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

        create_data = {"text": "test text"}
        assert db_session.query(Post).count() == 0
        response = client.post(url_posts_list, json=create_data, headers={"token": token})
        assert response.status_code == status.HTTP_200_OK
        assert db_session.query(Post).count() == 1
        post_db = db_session.query(Post).first()
        user_db = db_session.query(User).first()
        assert post_db.user == user_db
        assert post_db.user.username == data_register["username"]
        assert post_db.text == create_data["text"]

    def test_edit(
        self,
        test_db,
        client,
        db_session,
        url_posts_list,
        url_users_register,
        url_users_login,
        url_posts_detail,
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

        create_data = {"text": "test text"}
        assert db_session.query(Post).count() == 0
        response = client.post(url_posts_list, json=create_data, headers={"token": token})
        assert response.status_code == status.HTTP_200_OK
        assert db_session.query(Post).count() == 1
        post_db = db_session.query(Post).first()
        user_db = db_session.query(User).first()
        assert post_db.user == user_db
        assert post_db.user.username == data_register["username"]
        assert post_db.text == create_data["text"]

        edit_data = {"text": "new text"}
        response = client.patch(
            url_posts_detail.format(post_db.id), json=edit_data, headers={"token": token}
        )
        assert db_session.query(Post).count() == 1
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["info"] == f"Публикация {post_db.id} изменена"
        db_session.refresh(post_db)
        assert post_db.text == edit_data["text"]

    def test_delete(
        self,
        test_db,
        client,
        db_session,
        url_posts_list,
        url_users_register,
        url_users_login,
        url_posts_detail,
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

        create_data = {"text": "test text"}
        assert db_session.query(Post).count() == 0
        response = client.post(url_posts_list, json=create_data, headers={"token": token})
        assert response.status_code == status.HTTP_200_OK
        assert db_session.query(Post).count() == 1
        post_db = db_session.query(Post).first()
        user_db = db_session.query(User).first()
        assert post_db.user == user_db
        assert post_db.user.username == data_register["username"]
        assert post_db.text == create_data["text"]

        response = client.delete(url_posts_detail.format(post_db.id), headers={"token": token})
        assert db_session.query(Post).count() == 0
        assert response.status_code == status.HTTP_200_OK

    def test_like(
        self,
        test_db,
        client,
        db_session,
        url_posts_list,
        url_users_register,
        url_users_login,
        url_posts_detail,
        url_users_like,
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

        post = post_factory(db_session).create()
        db_session.commit()

        assert post.likes_count == 0
        response = client.post(url_users_like.format(post.id), headers={"token": token})
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "status": status.HTTP_200_OK,
            "info": f"Публикации {post.id} поставлен лайк",
        }
        assert db_session.query(Post).count() == 1
        db_session.refresh(post)
        assert post.likes_count == 1

    def test_like_error(
        self,
        test_db,
        client,
        db_session,
        url_posts_list,
        url_users_register,
        url_users_login,
        url_posts_detail,
        url_users_like,
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

        create_data = {"text": "test text"}
        assert db_session.query(Post).count() == 0
        response = client.post(url_posts_list, json=create_data, headers={"token": token})
        assert response.status_code == status.HTTP_200_OK
        assert db_session.query(Post).count() == 1
        post_db = db_session.query(Post).first()
        user_db = db_session.query(User).first()
        assert post_db.user == user_db
        assert post_db.user.username == data_register["username"]
        assert post_db.text == create_data["text"]

        assert post_db.likes_count == 0
        response = client.post(url_users_like.format(post_db.id), headers={"token": token})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Нельзя поставить лайк своей публикации."}
        assert db_session.query(Post).count() == 1
        db_session.refresh(post_db)
        assert post_db.likes_count == 0

    def test_dislike(
        self,
        test_db,
        client,
        db_session,
        url_posts_list,
        url_users_register,
        url_users_login,
        url_posts_detail,
        url_users_dislike,
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

        post = post_factory(db_session).create()
        db_session.commit()

        assert post.dislikes_count == 0
        response = client.post(url_users_dislike.format(post.id), headers={"token": token})
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "status": status.HTTP_200_OK,
            "info": f"Публикации {post.id} поставлен дизлайк",
        }
        assert db_session.query(Post).count() == 1
        db_session.refresh(post)
        assert post.dislikes_count == 1

    def test_dislike_error(
        self,
        test_db,
        client,
        db_session,
        url_posts_list,
        url_users_register,
        url_users_login,
        url_posts_detail,
        url_users_dislike,
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

        create_data = {"text": "test text"}
        assert db_session.query(Post).count() == 0
        response = client.post(url_posts_list, json=create_data, headers={"token": token})
        assert response.status_code == status.HTTP_200_OK
        assert db_session.query(Post).count() == 1
        post_db = db_session.query(Post).first()
        user_db = db_session.query(User).first()
        assert post_db.user == user_db
        assert post_db.user.username == data_register["username"]
        assert post_db.text == create_data["text"]

        assert post_db.dislikes_count == 0
        response = client.post(url_users_dislike.format(post_db.id), headers={"token": token})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Нельзя поставить дизлайк своей публикации."}
        assert db_session.query(Post).count() == 1
        db_session.refresh(post_db)
        assert post_db.dislikes_count == 0

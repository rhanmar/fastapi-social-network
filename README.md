# FastAPI Social Network

## Описание
* За основу взято [тестовое задание](https://docs.google.com/document/d/1_ZMjuXB0DnioQW7w30mrsA2WYzcdbWII4omgPvdPGQo/edit#heading=h.25xefdy4e9fk).
* Используется FastAPI, SQLAlchemy, Docker, PostgreSQL, SQLite.


## Запуск приложения
### С помощью Docker:
1. Клонировать репозиторий
2. `make build`
3. `make up`
4. Запуск тестов осуществляется командой `make test_backend`
5. Проверить доступ на http://localhost:8000/

### С помощью виртуального окружения:
1. `python3.10 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `make run`
5. Запуск тестов - `make test`
6. Проверить доступ на http://localhost:8000/

## API

* __GET__ `/docs`: документация 1
* __GET__ `/redoc`: документация 2
---
* __GET__ `/api/users/`: Список Пользователей
* __GET__ `/api/users/{user_id}`: Детальная информация о Пользователе
* __POST__ `/api/users/register`: Регистрация Пользователя
* __POST__ `/api/users/login`: Логин / получение токена
* __GET__ `/api/users/me`: Профиль Пользователя
---
* __GET__ `/api/posts/mine`: Публикации авторизированного Пользователя
* __GET__ `/api/posts/`: Список всех Публикаций
* __POST__ `/api/posts/`: Создание Публикации
* __GET__ `/api/posts/{post_id}`: Детальная информация о Публикации
* __DELETE__ `/api/posts/{post_id}`: Удаление Публикации
* __PATCH__ `/api/posts/{post_id}`: Измение Публикации
* __POST__ `/api/posts/{post_id}/like/`: Поставить лайк Публикации
* __POST__ `/api/posts/{post_id}/dislike/`: Поставить дизлайк Публикации

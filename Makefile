run:
	uvicorn app.main:app --reload

linters:
	black --config pyproject.toml app/
	isort --sp pyproject.toml app/
	#flake8 app/

test:
	pytest

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

exec_backend:
	docker-compose exec backend bash

exec_db:
	docker-compose exec db bash

test_backend:
	docker-compose exec backend pytest

update_requirements:
	pip freeze > requirements.txt

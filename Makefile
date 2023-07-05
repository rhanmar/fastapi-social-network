run:
	uvicorn app.main:app --reload

linters:
	black --config pyproject.toml app/
	isort --sp pyproject.toml app/
	#flake8 app/

test:
	pytest
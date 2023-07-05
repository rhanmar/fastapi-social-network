FROM python:3.11.0-slim
WORKDIR /app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
COPY requirements.txt .
COPY Makefile .
COPY pyproject.toml .
RUN pip install -r requirements.txt
COPY . .

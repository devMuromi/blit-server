FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /home/app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . .

RUN poetry run python manage.py collectstatic --noinput

CMD poetry run gunicorn your_project.wsgi:application --bind 0.0.0.0:8000

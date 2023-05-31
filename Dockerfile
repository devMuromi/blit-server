FROM python:3.9

ENV PYTHONUNBUFFERED=0

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl

RUN curl -sSL https://install.python-poetry.org | python -

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

COPY . .

RUN poetry run python manage.py collectstatic --noinput

CMD poetry run gunicorn config.wsgi:application --bind 0.0.0.0:8000
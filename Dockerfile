FROM python:3.9

ENV PYTHONUNBUFFERED=0

RUN apt update && \
    apt install -y python3-pip python3-dev && \
    apt install -y poetry && \
    apt-get clean 

WORKDIR /web

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi

COPY . .

RUN poetry run python manage.py collectstatic --noinput

CMD poetry run gunicorn your_project.wsgi:application --bind 0.0.0.0:8000
FROM python:3.9

ENV PYTHONUNBUFFERED=0

WORKDIR /app

RUN apt-get update && apt-get install -y

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

RUN poetry run python manage.py collectstatic --noinput

CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000
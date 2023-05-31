FROM python:3.10

ENV PYTHONUNBUFFERED=0

WORKDIR /web

COPY ./requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000
FROM ubuntu:18.04

ENV PYTHONUNBUFFERED=0

RUN apt-get update && \
    apt-get install -y python3-pip python3-dev && \
    apt-get clean

WORKDIR /web

COPY ./requirements.txt /web
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /web

RUN python manage.py collectstatic --noinput

CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000
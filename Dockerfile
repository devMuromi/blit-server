FROM python:3.10

ENV PYTHONUNBUFFERED=0

WORKDIR /web

COPY ./requirements.txt /web
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /web

RUN python manage.py collectstatic --noinput

EXPOSE 80

CMD gunicorn config.wsgi --bind 0.0.0.0:80
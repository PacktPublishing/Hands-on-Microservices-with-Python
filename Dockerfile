FROM python:3-alpine

MAINTAINER Peter Fisher

COPY ./app /app

WORKDIR /app

RUN apk add --update \
    py-mysqldb \
    gcc \
    libc-dev \
    mariadb-dev \
  && pip install -r requirements.txt \
  && rm -rf /var/cache/apk/*

CMD ["python", "app.py"]


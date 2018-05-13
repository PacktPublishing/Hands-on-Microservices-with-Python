FROM python:3-alpine

MAINTAINER Peter Fisher

COPY app /app

WORKDIR /app

RUN pip install -r requirments.txt

CMD ["python", "app.py"]


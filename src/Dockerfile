# Dockerfile for penny-analytics realtime API
FROM ubuntu:19.04

MAINTAINER Pimin Konstantin Kefaloukos "pimin.konstantin.kefaloukos@maersk.com"

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip libpq-dev

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY *.py /

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "app:app", "-k", "sync"]

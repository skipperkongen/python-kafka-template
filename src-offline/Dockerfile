# Dockerfile for offline action service
FROM ubuntu

MAINTAINER Pimin Konstantin Kefaloukos "pimin.konstantin.kefaloukos@maersk.com"

RUN apt-get update -y
RUN apt-get install -y python3-pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY kafka_producer.py .
COPY kafka_consumer.py .

FROM python:3.8.2-slim-buster

RUN mkdir -p /app

WORKDIR /app
COPY ./ /app/

RUN apt-get update
RUN apt-get install -y python3-pip

RUN pip install -r requirements.txt

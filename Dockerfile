FROM python:3.7.1-stretch

RUN mkdir -p /app

WORKDIR /app
COPY ./ /app/

RUN apt-get update
RUN apt-get install -y python3-pip

RUN pip install -r requirements.txt

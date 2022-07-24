FROM python:3.10-slim-buster

ARG POETRY_VERSION=1.1.12

ENV PYTHONUNBUFFERED=1
RUN apt update && apt install ffmpeg -y

WORKDIR /worker

COPY requirements.txt /worker 

RUN ["pip", "install", "-r", "requirements.txt"]

COPY . /worker

RUN chmod +x /worker/entrypoint.sh

ENTRYPOINT ["/worker/entrypoint.sh"]

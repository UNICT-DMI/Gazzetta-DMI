# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /app

RUN mkdir tmp

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "main.py"]

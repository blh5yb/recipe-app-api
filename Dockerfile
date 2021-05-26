FROM python:3.7-alpine
MAINTAINER Barry Hykes Jr

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

#-D for running app only - security purposes
RUN adduser -D user
USER user

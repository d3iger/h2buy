#!/usr/bin/env bash
# syntax=docker/dockerfile:1

FROM python:3.10.0-slim-buster

WORKDIR /Users/matviy/PycharmProjects/H2BUY

RUN apt-get update
RUN apt-get -y install gcc

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "main-h2buy", "run", "--host=0.0.0.0"]
FROM python:latest

RUN apt-get update

RUN apt-get install -y curl git docker.io

RUN pip --version


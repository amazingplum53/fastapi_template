FROM python:latest

RUN apt-get update

RUN apt-get install -y curl git docker.io awscli 

RUN curl -fsSL https://get.pulumi.com | sh

RUN git --version && pip --version && docker --version && pulumi version && aws --version

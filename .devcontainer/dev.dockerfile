FROM python:latest

WORKDIR /workspace/decouple/

RUN apt-get update

RUN apt-get install -y curl git docker.io awscli 

RUN curl -fsSL https://get.pulumi.com | sh

ENV PATH="/root/.pulumi/bin:${PATH}"

# Verify packages are installed correctly
RUN git --version && pip --version && docker --version && pulumi version && aws --version 

RUN git config --global user.name "Matthew"
RUN git config --global user.email "matthewpaulh@hotmail.co.uk"

RUN pip install uv


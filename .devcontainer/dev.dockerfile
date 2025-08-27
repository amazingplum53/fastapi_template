FROM python:latest

WORKDIR /workspace/fastapi_template/

COPY dev.requirements.txt /tmp/dev.requirements.txt

RUN apt-get update

RUN apt-get install -y curl git docker.io awscli less

RUN curl -fsSL https://get.pulumi.com | sh

ENV PATH="/root/.pulumi/bin:${PATH}"

# Verify packages are installed correctly
RUN git --version && pip --version && docker --version && pulumi version && aws --version 

RUN pip install uv

RUN uv pip install -r /tmp/dev.requirements.txt --system


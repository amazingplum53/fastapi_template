FROM python:latest

RUN apt-get update

RUN apt-get install -y curl git docker.io awscli 

RUN curl -fsSL https://get.pulumi.com | sh

ENV PATH="/root/.pulumi/bin:${PATH}"

# Verify packages are installed correctly
RUN git --version && pip --version && docker --version && pulumi version && aws --version 

RUN pip install uv
RUN uv pip install -r /workspace/decouple/.devcontainer/dev.requirements.txt --system

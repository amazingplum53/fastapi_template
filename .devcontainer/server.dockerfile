FROM python:latest

ENV BASEDIR="/server/" 
ENV PROJECT_NAME="fastapi_template" 

RUN mkdir $BASEDIR $BASEDIR/$PROJECT_NAME

WORKDIR $BASEDIR/$PROJECT_NAME

COPY . .

RUN pip install uv

RUN uv pip install -r .devcontainer/server.requirements.txt --system

#HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
#CMD curl -f http://localhost:8000/ || exit 1

CMD ["python", "${PROJECT_NAME}/asgi.py"] 


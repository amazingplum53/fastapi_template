FROM python:latest

ENV BASEDIR="/server/" 

RUN mkdir $BASEDIR $BASEDIR/decouple

WORKDIR $BASEDIR/decouple

COPY . .

RUN pip install uv

RUN uv pip install -r .devcontainer/server.requirements.txt --system

CMD [".devcontainer/setup_container.sh" "&&" "gunicorn", "decouple.wsgi", "-c", "decouple/gunicorn.config.py"]

FROM python:latest

ENV BASEDIR="/server/" 

RUN mkdir $BASEDIR

RUN git clone https://github.com/amazingplum53/decouple_test.git $BASEDIR/decouple/

WORKDIR $BASEDIR/decouple

RUN pip install uv
RUN uv pip install -r .devcontainer/server.requirements.txt --system

CMD ["gunicorn", "decouple.wsgi", "-c", "decouple/gunicorn.config.py"]

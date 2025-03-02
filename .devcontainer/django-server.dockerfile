FROM python:latest

ENV BASEDIR="/server/" 

RUN git clone https://github.com/amazingplum53/decouple_test.git $BASEDIR/decouple/

WORKDIR $BASEDIR/decouple

RUN pip install uv
RUN uv pip install -r .devcontainer/requirements.txt --system

CMD ["gunicorn", "portfolio.wsgi", "-c", "gunicorn.config.py"]

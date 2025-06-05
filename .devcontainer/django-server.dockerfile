FROM python:latest

ENV BASEDIR="/server/" 

RUN mkdir $BASEDIR $BASEDIR/decouple

WORKDIR $BASEDIR/decouple

COPY . .

RUN pip install uv

RUN uv pip install -r .devcontainer/server.requirements.txt --system

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
CMD curl -f http://localhost:8000/ || exit 1

CMD ["gunicorn", "decouple.wsgi", "-c", "decouple/gunicorn.config.py"]

FROM python:latest

ENV BASEDIR="/server/" 

RUN git clone https://github.com/amazingplum53/decouple_test.git $BASEDIR/decouple/

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

RUN pip install uv
RUN uv pip install -r .devcontainer/requirements.txt --system

WORKDIR $BASEDIR/decouple

CMD ["sleep", "infinity"]

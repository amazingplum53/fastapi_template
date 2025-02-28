FROM python:latest

ENV BASEDIR="/server/" 

RUN git clone https://github.com/amazingplum53/decouple_test.git $BASEDIR/decouple/

WORKDIR $BASEDIR/decouple

CMD ["sleep", "infinity"]

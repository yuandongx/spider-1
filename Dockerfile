FROM python:3.13-alpine3.21

ENV logs=/app/logs

RUN mkdir /app

COPY api /app/api

COPY spider /app/spider

COPY gunconfig.py /app/api/gunconfig.py

COPY start.sh /app/start.sh
COPY requirements.txt  /app/requirements.txt

RUN pip install -r /app/requirements.txt

ENTRYPOINT [ "/bin/bash", "/app/start.sh"]
FROM python:3.13-alpine3.21

ENV logs=/app/logs

RUN mkdir /app

COPY . /app

RUN /usr/local/bin/pip install -r /app/requirements.txt

ENTRYPOINT [ "/bin/sh", "/app/start.sh"]
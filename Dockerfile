FROM app-base:latest

ENV logs=/app/logs

RUN mkdir /app

COPY . /app

RUN /usr/local/bin/pip install -r /app/requirements.txt

WORKDIR /app

ENTRYPOINT [ "/bin/sh", "/app/start.sh"]
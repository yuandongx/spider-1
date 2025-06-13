FROM dong01/app-base

ENV logs=/app/logs

RUN mkdir /app

COPY . /app

RUN pip install --no-cache-dir -r /app/requirements.txt;\
    rm -rf ~/.cache/pip/http-v2

WORKDIR /app

# ENTRYPOINT [ "/bin/sh", "/app/start.sh"]
CMD [ "tail", "-10f", "/dev/null"]

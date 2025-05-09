#!/bin/bash

for i in `ps -ef | grep 'celery' | grep -v grep | awk '{print $3}'`
do
    echo "kill $i"
    kill -9 $i
done

echo Celery beat is starting...
celery -A spider beat --loglevel info --logfile $CELERY_BEAT_LOG --schedule $CELERY_SCHEDULE_FILE --detach

echo Celery worker is starting...
celery -A spider worker --concurrency 3 --loglevel info --logfile $CELERY_WORKER_LOG
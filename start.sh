#!/bin/sh

LOGS=logs
DATA='data'
CELERY_SCHEDULE_FILE='data/celery.beat.schedule'
CELERY_WORKER_LOG='logs/celery.worker.log'
CELERY_BEAT_LOG='logs/celery.beat.log'

if [ -d "$LOGS" ];then
    echo 'logs dir is exists.'
else
    mkdir $LOGS
fi

if [ -d "$DATA" ]; then
    echo 'data dir is exists.'
else
    mkdir $DATA
fi
echo Start app server...

# python -m gunicorn -c gunconfig.py main:app
python  main.py


#echo Celery beat is starting...
#celery -A spider beat --loglevel  info --logfile $CELERY_BEAT_LOG --schedule $CELERY_SCHEDULE_FILE --detach
#
#echo Celery worker is starting...
#celery -A spider worker --concurrency 3 --loglevel  info --logfile $CELERY_WORKER_LOG
# celery -A spider worker -l info -P processes -detach

#tail -200f /dev/null
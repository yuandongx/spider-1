#!/bin/bash

# This script is used to restart the Celery worker and beat processes.
# It kills any existing Celery processes and starts new ones.
# It also creates necessary directories and log files if they do not exist.
# Usage: ./re-start-celery.sh


# Check if the Redis log directory exists, if not create it
if [ -d "/var/log/redis" ]; then
    echo "var/log/redis is exist."
else
    mkdir /var/log/redis
fi

ps -ef | grep 'redis-server' | grep -v grep
if [ $? -ne 0 ]; then
    echo "Redis server is not running. Start Redis server first."
    redis-server ./setup/redis.conf &
    sleep 3
fi

# Check if the logs directory exists, if not create it
if [ ! -d "logs" ]; then
    mkdir logs
    echo 'logs dir created.'
fi

# Check if the celery.beat.log file exists, if not create it
if [ -f "$CELERY_BEAT_LOG" ]; then
    echo 'CELERY_BEAT_LOG is exists.'
else
    CELERY_BEAT_LOG='logs/celery.beat.log'
    echo 'CELERY_BEAT_LOG created.'
fi

# Check if the celery.worker.log file exists, if not create it
if [ -f "$CELERY_WORKER_LOG" ]; then
    echo 'CELERY_WORKER_LOG is exists.'
else
    CELERY_WORKER_LOG='logs/celery.worker.log'
    echo 'CELERY_WORKER_LOG created.'
fi

# Kill any existing Celery processes
echo Killing existing Celery processes...
ps -ef | grep 'celery' | grep -v grep|grep -v 'setup/re-start-celery.sh' 
for i in `ps -ef | grep 'celery' | grep -v grep | awk '{print $2}'`
do
    # kill -9 $i
    echo "Killed process $i"
done

# Start the Celery beat and worker processes
echo Starting Celery processes...
celery -A spider beat --loglevel info --logfile $CELERY_BEAT_LOG --schedule $CELERY_SCHEDULE_FILE --detach

# Start the Celery worker process
echo Starting Celery worker...
celery -A spider worker --concurrency 3 --loglevel info --logfile $CELERY_WORKER_LOG
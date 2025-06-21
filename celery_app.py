import  os

from loguru import logger
from spider import app


def start_celery():
    """
    Called just before the master process is initialized.
    
    # echo Celery beat is starting...
    # celery -A spider beat --loglevel  info --logfile $CELERY_BEAT_LOG --schedule $CELERY_SCHEDULE_FILE --detach
    #
    # echo Celery worker is starting...
    # celery -A spider worker --concurrency 3 --loglevel  info --logfile $CELERY_WORKER_LOG
    # celery -A spider worker -l info -P processes --detach

    """
    celery_worker_log = os.getenv("CELERY_WORKER_LOG") or "logs/celery.worker.log"

    celery_beat_log = os.getenv("CELERY_BEAT_LOG") or "logs/celery.beat.log"

    celery_schedule_file = os.getenv("CELERY_SCHEDULE_FILE") or "logs/celery.schedule.log"

    logger.info('Celery is starting...')

    args = ["-A spider", "worker", "--concurrency 3", "--loglevel  info", f"--logfile {celery_worker_log}"]
    app.worker_main(args)

    args = ["-A spider", "beat", " --loglevel  info", f"--logfile {celery_beat_log}", f"--schedule {celery_schedule_file}", "--detach"]
    app.beat_main(args)

if __name__ == '__main__':
    start_celery()
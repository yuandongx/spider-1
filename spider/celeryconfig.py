"""
celery config
"""
from celery.schedules import crontab

enable_utc = True
timezone = 'Asia/Shanghai'
result_backend = 'redis://127.0.0.1:6379/0'
broker_url = 'redis://127.0.0.1:6379/0'
beat_schedule = {
    "sina_hq0": {
        "task": "spider.sina_hq",
        "schedule": crontab(hour='9-11', day_of_week='1-5', minute='*'),
    },
    "sina_hq1": {
        "task": "spider.sina_hq",
        "schedule": crontab(hour='13-14', day_of_week='1-5', minute='*'),
    },
    "sina_hq2": {
        "task": "spider.sina_hq",
        "schedule": crontab(hour='15', day_of_week='1-5', minute='1'),
    }
}

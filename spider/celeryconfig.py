"""
celery config
"""
from celery.schedules import crontab

enable_utc = True
timezone = 'Asia/Shanghai'
result_backend = 'redis://127.0.0.1:6379/0'
broker_url = 'redis://127.0.0.1:6379/0'
beat_schedule = {
    "xueqiu_hq": {
        "task": "spider.xueqiu_hq",
        "schedule": crontab(hour=15, minute='*'),
    }
}

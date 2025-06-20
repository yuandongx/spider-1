"""
celery config
"""
import os
from celery import Celery

from db import Mgdb

# app data dir 
app_data_dir = os.getenv('APP_DTA_DIR', './data')
app_redis = os.getenv('APP_REDIS', 'redis://127.0.0.1:6379/0')

# mongodb 
mgdb = Mgdb()

app = Celery(
    "task_runner",
    broker=app_redis,
    backend=app_redis
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
)


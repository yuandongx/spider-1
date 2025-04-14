"""
celery config
"""
from huey import SqliteHuey


# Create a Huey instance with SQLite as the backend
huey = SqliteHuey('tasks.db', auto_commit=True, store_none=True)
# Set the timezone to UTC
huey.timezone = 'Asia/Shanghai'
# Set the result expiration time to 7 days
huey.result_expiration = 3600*24*7
# Set the task retry delay to 10 seconds
huey.retry_delay = 10
# Set the task retry limit to 5
huey.retry_limit = 5
# Set the task timeout to 60 seconds
huey.task_timeout = 60
# Set the task queue name
huey.task_queue = 'tasks'
# Set the task result queue name
huey.result_queue = 'results'
# Set the task error queue name
huey.error_queue = 'errors'
# Set the task retry queue name
huey.retry_queue = 'retries'
# Set the task success queue name
huey.success_queue = 'success'
# Set the task failure queue name
huey.failure_queue = 'failure'
# Set the task timeout queue name
huey.timeout_queue = 'timeout'
# Set the task retry delay queue name
huey.retry_delay_queue = 'retry_delay'
# Set the task retry limit queue name
huey.retry_limit_queue = 'retry_limit'
# Set the task result expiration queue name
huey.result_expiration_queue = 'result_expiration'
# Set the task result queue name
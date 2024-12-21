from pathlib import Path
import os

from uvicorn.workers import UvicornWorker
from dotenv import load_dotenv

load_dotenv()

root_path=Path(__file__).absolute().parent

logs_path = root_path.joinpath('logs')
if not logs_path.exists():
    os.mkdir(logs_path)

accesslog=logs_path.joinpath('access.log').as_posix()

errorlog=logs_path.joinpath( 'error.log').as_posix()

pidfile=logs_path.joinpath('pidfile.log').as_posix()

loglevel='info'

bind = "127.0.0.1:8000"

proc_name='spider1'

daemon=True

worker_class=UvicornWorker
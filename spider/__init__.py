from celery import Celery
from redis import Redis
from loguru import logger
from .fetch.sina import get_hq_node_data as get_sina_hq_data
from .db import Mgdb

mgdb = Mgdb()

app = Celery()

app.config_from_object("spider.celeryconfig")


@app.task
def sina_hq():
    """ 
    sina_hq
    """
    payload = {"page": 1,
               "size": 60,
               "order": "desc",
               "order_by": "percent",
               "market": "CN",
               "type": "sha"}
    res = get_sina_hq_data(payload)
    data = {
        "db": "stock",
        "collection": "hq",
        "data": res
    }
    mgdb.insert_or_update(data)




if __name__ == '__main__':
    args = []
    app.worker_main

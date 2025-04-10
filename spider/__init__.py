from celery import Celery
from loguru import logger

from fetch.sina import get_hq_node_data as get_sina_hq_data
from db import Mgdb

mgdb = Mgdb()

# app = Celery()

# app.config_from_object("spider.celeryconfig")


# @app.task
def sina_hq():
    """ 
    hs_a
    sz_a
    hs_bjs
    """
    for node in ('hs_a', 'sz_a', 'hs_bjs'):
        payload = {"page": 1,
                "size": 60,
                "order": "desc",
                "order_by": "percent",
                "market": "CN",
                "node": "sh_a"}
        res = get_sina_hq_data(payload)
        data = {
            "db": "stock",
            "collection": "hq",
            "data": res
        }
        mgdb.insert_or_update(data)




if __name__ == '__main__':
    sina_hq()

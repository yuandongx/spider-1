from celery import Celery
from redis import Redis
from loguru import logger
from .fetch.xueqiu import XQrequest
from .db import Mgdb

mgdb = Mgdb()

app = Celery()

app.config_from_object("spider.celeryconfig")

# logger.add()


@app.task
def xueqiu_hq():
    """ 
    xueqiu_hq
    """
    xq = XQrequest(db=mgdb)
    payload = {"page": 1,
               "size": 60,
               "order": "desc",
               "order_by": "percent",
               "market": "CN",
               "type": "sha"}
    res = xq.get_hq_data(payload)
    print(res)

@app.task
def xueiqu_stock():
    """ 
    xueqiu stock
    """
    r = Redis(host='127.0.0.1', port=6379, db=1, decode_responses=True)
    all_elements = r.lrange('myfllows', 0, -1)
    xq = XQrequest(db=mgdb)
    result = []
    for item in all_elements:
        params = {
            "symbol": item,
            "extend": "detail"
        }
        res = xq.get_stock(params)
        result.append(res)
        logger.info(f'[{item}]>>>>>{res}')
    return result


if __name__ == '__main__':
    xueqiu_hq.apply()


# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : __init__.py
# @Software: vscode
# @Description:
"""
工厂处理
"""
from datetime import datetime

from celery import Celery
# from loguru import logger

from .fetch.ak import get_realtime_data
from .fetch.sina import get_hq_node_data as get_sina_hq_data
from .db import Mgdb
from .config import huey as app

mgdb = Mgdb()


@app.task
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


@app.task
def ak_realtime():
    """
    获取实时数据
    """
    data = get_realtime_data()
    date = datetime.now().strftime('%Y-%m-%d')
    payload = {
        "db": "stock",
        "collection": date,
        "data": data
    }
    mgdb.insert_or_update(payload)

if __name__ == '__main__':
    sina_hq()

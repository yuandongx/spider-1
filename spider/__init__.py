
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

from loguru import logger

from .fetch.ak import get_realtime_data
from .fetch.sina import get_hq_node_data as get_sina_hq_data, NODES

from .config import huey as app, mgdb


@app.task()
def sina_hq():
    """ 
    hs_a
    sz_a
    hs_bjs
    """
    date = datetime.now().strftime('%Y%m%d')
    for node in NODES:
        res = get_sina_hq_data(node)
        payload = {
            "db": "stock",
            "collection": date,
            "data": res['data']
        }
        mgdb.insert_or_update(payload)
  

@app.task()
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
    return data


if __name__ == '__main__':
    sina_hq()

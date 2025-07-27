
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
from celery.schedules import crontab
from loguru import logger

from .fetch.ak import get_realtime_data
from .fetch.sina import get_hq_node_data as get_sina_hq_data, NODES

from .config import app, mgdb


@app.task
def sina_hq():
    """ 
    hs_a
    sz_a
    hs_bjs
    """
    logger.info('【sina_hq】is running...')
    date = datetime.now().strftime('%Y%m%d')
    for node in NODES:
        res = get_sina_hq_data(node)
        payload = {
            "db": "stock",
            "collection": date,
            "data": res['data']
        }
        mgdb.insert_or_update(payload)
  

@app.task
def ak_realtime():
    """
    获取实时数据
    """
    logger.info('【ak_realtime】is running...')
    data = get_realtime_data()
    date = datetime.now().strftime('%Y-%m-%d')
    payload = {
        "db": "stock",
        "collection": date,
        "data": data
    }
    mgdb.insert_or_update(payload)
    return data



@app.on_after_configure.connect
def set_up_add_periodic_tasks(sender: Celery, **kwargs):

    sender.add_periodic_task(crontab(minute="*/3",
                                     hour="9,10,11,13,14",
                                     day_of_week="1-5"),
                            sina_hq.s(),
                            name="sina_hq1")
    
    sender.add_periodic_task(crontab(minute="*/3",
                                     hour="9,10,11,13,14",
                                     day_of_week="1-5"),
                            ak_realtime.s(),
                            name="ak_realtime1")
    


if __name__ == '__main__':
    sina_hq()

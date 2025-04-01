
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : __init__.py
# @Software: vscode
# @Description:
"""
工厂处理
"""
from celery import Celery
from celery.schedules import crontab

from .ak import realtime, history
from .sina import sina_hq as get_sina_hq_data
from .config import app


@app.task
def sina_hq():
    """ 
    hs_a
    sz_a
    hs_bjs
    """
    return get_sina_hq_data()
  

@app.task
def ak_realtime():
    """
    获取实时数据
    """
    return realtime()

@app.task
def ak_history():
    """
    获取历史数据
    """
    return history()

@app.on_after_configure.connect
def set_up_add_periodic_tasks(sender: Celery, **kwargs):
    # 定时任务 
    # 每天9点到11点，每3分钟执行一次
    # 每天13点到14点，每3分钟执行一次
    sender.add_periodic_task(crontab(minute="*/3",
                                     hour="9,10,11,13,14",
                                     day_of_week="0-4"),
                            sina_hq.s(),
                            name="sina_hq1")
    # 每天1点执行一次
    # 每天9点到11点，每3分钟执行一次
    # 每天13点到14点，每3分钟执行一次
    # 每天1点执行一次
    sender.add_periodic_task(crontab(minute="*/3",
                                     hour="9,10,11,13,14",
                                     day_of_week="0-4"),
                            ak_realtime.s(),
                            name="ak_realtime1")
    
    # 每天1点执行一次
    sender.add_periodic_task(crontab(minute="0",
                                     hour="1",
                                     day_of_week="2,5"),
                            ak_history.s(),
                            name="ak_history")


if __name__ == '__main__':
    sina_hq()

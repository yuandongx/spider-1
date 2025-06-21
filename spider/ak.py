# -*- coding: utf-8 -*-
# @Time    : 
from datetime import datetime
from loguru import logger

from .fetch.ak import get_realtime_data , get_stock_zh_a_history
from .config import mgdb

def realtime():
    """
    获取实时数据
    """
    logger.info('【ak_realtime】is running...')
    data = get_realtime_data()
    payload = {
        "db": "realtime",
        "collection": 'all',
        "data": data
    }
    mgdb.insert_or_update(payload)
    return data


def history():
    """
    获取历史数据
    """
    now = datetime.now()
    _now = now.strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f'{_now}|ak_historyis running...')
    codes = mgdb.get_latest_all_stock()
    logger.info(f"获取最新的所有股票数据: {len(codes)}")
    not_goods = []
    for symbol in codes:
        try:
            data = get_stock_zh_a_history(symbol)
            payload = {
                "db": "default",
                "collection": symbol,
                "data": data
            }
            mgdb.insert_or_update(payload)
        except Exception as e:
            logger.error(f"获取股票 {symbol} 历史数据失败: {e}")
            not_goods.append(symbol)
            continue
    # 获取所有股票数据
    uesed = datetime.now() - now
    logger.info(f"获取历史数据完成, 耗时: {uesed.total_seconds()}秒")

def update_history():
    """
    获取历史数据重试
    """
    now = datetime.now()
    _now = now.strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f'{_now}|update_history is running...')
    codes = mgdb.get_latest_all_stock()
    count = len(codes)
    logger.info(f"获取最新的所有股票数据: {count}")
    records = []
    for index, item in enumerate(codes):
        logger.info(f"【{index+1}/{count}】获取股票 {item['idx']} 历史数据...")
        try:
            data = get_stock_zh_a_history(item['code'], limit=60)
            records.append({'idx': item['idx'], '历史': data})
        except Exception as e:
            logger.error(f"获取股票 {item['idx']} 历史数据失败: {e}")
            continue
    payload = {
        "db": "default",
        "collection": 'all',
        "data": records
    }
    mgdb.insert_or_update(payload)
    # 获取所有股票数据
    uesed = datetime.now() - now
    logger.info(f"获取历史数据完成, 耗时: {uesed.total_seconds()}秒")
   
if __name__ == '__main__':
    # res = get_realtime_data()
    # print(res)
    res = realtime()
    print(res)
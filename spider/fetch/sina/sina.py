"""
get data from sina
"""
from datetime import datetime
from typing import Any

import requests
from loguru import logger

# sgt_sz
# hgt_sh
# hs_bjs
NODES = [
    "sgt_sz",
    "hgt_sh",
    "hs_bjs",
    "kcb",
    "cyb"
]
# https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=40&sort=changepercent&asc=1&node=hs_a&symbol&_s_r_a=init


def get(url, payload=None) -> Any | None:
    """
    base method: get data
    """
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "User-Agent": "insomnia/9.3.0-beta.6",
        "Connection": "keep-alive"
    }
    resp = requests.get(url, params=payload, headers=headers, timeout=30)
    if resp.status_code == 200:
        return resp.json()
    else:
        return None


def get_hq_count(node: str):
    """
    > hgt_sh
    
    """    
    url = f'https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount?node={node}'
    data = get(url)
    if isinstance(data, str) and data.isdigit():
        return int(data)
    return 0


def get_hq_data(params):
    """
    get hang qing data
    """
    json_api = 'https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData'
    # page=1&num=40&sort=changepercent&asc=1&node=hs_a&symbol&_s_r_a=init

    payload = params.get('payload') 
    res = get(json_api, payload)
    if res is None:
        return
    date = datetime.now().strftime('%Y%m%d')
    rtn = []
    for item in res:
        item['idx'] = f'{date}@{item["symbol"]}'
        item['node'] = payload['node']
        item['date'] = date
        rtn.append(item)
    return rtn


def get_hq_node_data(data):
    """
    按node查询行情
    """
    result = []
    _now = datetime.now()
    count = get_hq_count('sh_a')
    logger.info(f'Got hgt_sh count {count}.')
    p, m = divmod(count, 40)
    if m > 0:
        pages = p + 2
    else:
        pages = p + 1
    for i in range(1, pages):

        payload = {"page": i,
               "num": 40,
               "sort": "changepercent",
               "asc": 1,
               "symbol": "",
               "node": 'sha',
               "_s_r_a": "init"}
        payload.update(data)
        rtn = get_hq_data({"payload": payload, "node": data['node']})
        if rtn is not None and isinstance(rtn, list):
            result.extend(rtn)
    _spend = datetime.now() - _now
    logger.info(f'Got {count} items in {_spend.seconds}s.')
    return result


def get_top100(acs=0):
    # https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?
    # page=1&num=40&sort=changepercent&asc=1&node=hs_a&symbol=&_s_r_a=init
    # https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?
    # page=1&num=40&sort=changepercent&asc=1&node=hs_a&symbol=&_s_r_a=init
    result = []
    for i in (1,2,3):
        params = { "page": i,
                    "num": 40,
                    "sort": "changepercent",
                    "asc": acs,
                    "symbol": "",
                    "node": 'hs_a',
                    "_s_r_a": "init"}
        rtn = get_hq_data({"payload": params, "node": "node"})
        result.append(rtn)

def get_up100():
    return get_top100()

def get_down100():
    return get_top100(1)


if __name__ == '__main__':
    # sgt_sz
    # hgt_sh
    # hs_bjs
    rs = get_hq_node_data("kcb")
    print(rs)

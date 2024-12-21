"""
get data from sina
"""
from datetime import datetime
import requests


# https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=40&sort=changepercent&asc=1&node=hs_a&symbol&_s_r_a=init


def get(url, payload=None) -> dict:
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


def get_hq_data(params):
    """
    get hang qing data
    """
    json_api = 'https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData'
    # page=1&num=40&sort=changepercent&asc=1&node=hs_a&symbol&_s_r_a=init
    default = {"page": 1,
               "num": 60,
               "sort": "changepercent",
               "asc": 1,
               "symbol": "",
               "node": "hs_a",
               "_s_r_a": "init"}
    payload = params.get('payload') or default
    res = get(json_api, payload)
    date = datetime.now().strftime('%Y%m%d')
    rtn = []
    for item in res:
        item['idx'] = f'{date}@{item["symbol"]}'
        item['node'] = payload['node']
        item['date'] = date
        rtn.append(item)
    return rtn


if __name__ == '__main__':
    rs = get_hq_data({})
    print(rs)

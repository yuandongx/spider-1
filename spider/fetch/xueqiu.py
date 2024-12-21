from datetime import datetime
import requests
from .sample import xue_qiu_stock, xue_qiu_hq
# https://xueqiu.com/
# url = "https://xueqiu.com/"
# https://stock.xueqiu.com/v5/stock/screener/quote/list.json


class XQrequest:

    base_url = 'https://xueqiu.com/'
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "User-Agent": "insomnia/9.3.0-beta.6",
        "Connection": "keep-alive"
    }

    def __init__(self, db=None) -> None:
        self._session = requests.Session()
        self._cookie = []
        self.db = db
        self._init()

    def _init(self) -> None:
        payload = {}
        headers = {
            "Accept": "*/*",
            "Content-Type": "text/html",
            "User-Agent": "insomnia/9.3.0-beta.6"
        }

        res = self._session.get(self.base_url, headers=headers, data=payload)
        if res.status_code == 200:
            for item in res.cookies.items():
                self._cookie.append('{}={}'.format(*item))

    def get(self, url, payload=None) -> dict:
        res = self._session.get(url=url, params=payload, headers=self.headers)
        if res.status_code == 200:
            return res.json()
        else:
            return {}
    
    def get_hq_data(self, payload):
        json_api = 'https://stock.xueqiu.com/v5/stock/screener/quote/list.json'
        response = self.get(json_api, payload)
        if data := response.get('data'):
            items = data.get('list', [])
            if self.db is not None:
                values =[]
                for item in items:
                    item['node'] = payload['type']
                    values.append(xue_qiu_hq(item))
                params = {
                    'db': 'stock',
                    'collection': 'hq',
                    'data': values
                }
                self.db.insert_or_update(params)
            return items
        else:
            return []
    
    def get_stock(self, params):
        _url = 'https://stock.xueqiu.com/v5/stock/quote.json'
        response = self.get(_url, params)
        if data := response.get('data'):
            status = data.get('market', {}).get('status')
            quote = data.get('quote', {})
            error_code = data.get('error_code', 0)
            quote['status'] = status
            params = {
                    'db': 'stock',
                    'collection': 'myfllows',
                    'data': [xue_qiu_stock(quote)]
            }
            return self.db.insert_or_update(params)


if __name__ == '__main__':
    xq = XQrequest()
    # payload = {"page": 1,
    #            "size": 60,
    #            "order": "desc",
    #            "order_by": "percent",
    #            "market": "CN",
    #            "type": "sha"}
    # res = xq.get_hq_data(payload)
    params = {
        "symbol": "SZ002625",
        "extend": "detail"
    }
    res = xq.get_stock(params)
    print(res)

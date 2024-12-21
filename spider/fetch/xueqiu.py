import requests

# https://xueqiu.com/
# url = "https://xueqiu.com/"
# https://stock.xueqiu.com/v5/stock/screener/quote/list.json


class XQrequest:

    base_url = 'https://xueqiu.com/'
    json_api = 'https://stock.xueqiu.com/v5/stock/screener/quote/list.json'
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "User-Agent": "insomnia/9.3.0-beta.6",
        "Connection": "keep-alive"
    }

    def __init__(self) -> None:
        self._session = requests.Session()
        self._cookie = []
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

    def get(self, payload=None) -> dict:
        res = self._session.get(url=self.json_api, params=payload,
                                headers=self.headers)
        if res.status_code == 200:
            return res.json()
        else:
            return {}

    def post(self, payload=None) -> dict:
        pass


if __name__ == '__main__':
    xq = XQrequest()
    payload = {"page": 1,
               "size": 60,
               "order": "desc",
               "order_by": "percent",
               "market": "CN",
               "type": "sha"}
    xq.get(payload)

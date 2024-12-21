
import requests


# https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=40&sort=changepercent&asc=1&node=hs_a&symbol&_s_r_a=init


class Sina:

    base_url = 'https://xueqiu.com/'
    json_api = 'https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData'
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

if __name__ == '__main__':
    xq = Sina()
    # page=1&num=40&sort=changepercent&asc=1&node=hs_a&symbol&_s_r_a=init
    payload = {"page": 1,
               "num": 60,
               "sort": "changepercent",
               "asc": 1,
               "symbol": "",
               "node": "hs_a",
               "_s_r_a": "init"}
    res =  xq.get(payload)
    print(res)

from requests_html import HTMLSession
from lxml.etree import ElementTree, fromstring
from bs4 import BeautifulSoup

def fetch_html(url):
    session = HTMLSession()
    res = session.get(url)
    print(res.html.find('.m-table'))


def parse_html(html):
    root = BeautifulSoup(html, 'html')
    print()


if __name__ == '__main__':
    # fetch_html('http://data.10jqka.com.cn/market/longhu/')
    with open('/home/develop/workspace/spider-1/data/1.html', 'r', encoding='utf-8') as f:
        data = f.read()
        parse_html(data)

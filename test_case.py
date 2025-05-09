"""
111111
"""
from .config import load_config
from .spider.main import sina_hq

if __name__ == '__main__':
    load_config()
    res = sina_hq()
    res()

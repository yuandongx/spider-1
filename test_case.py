"""
111111
"""
from dotenv import load_dotenv
from spider.main import sina_hq

load_dotenv()
if __name__ == '__main__':
    res = sina_hq()
    res()

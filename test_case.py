"""
111111
"""
from config import load_config
from spider import get_sina_hq_data

if __name__ == '__main__':
    load_config()
    res = get_sina_hq_data()
  

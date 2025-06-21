"""
111111
"""
from config import load_config
from spider import update_history

if __name__ == '__main__':
    load_config()
    res = update_history()
  

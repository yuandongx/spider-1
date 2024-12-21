"""
数据格式标准化
"""
from datetime import datetime
from pathlib import Path
import json


with Path(__file__).absolute().parent.joinpath('template', 'hq-base.json').open('r', encoding='utf-8') as f:
    base = json.load(f)
with Path(__file__).absolute().parent.joinpath('template', 'stock-base.json').open('r', encoding='utf-8') as f:
    stock = json.load(f)

def _(tamplate, item):
    data = {}
    _idx = datetime.now().strftime("%y%m%d")
    for k in tamplate.keys():
        if k in item:
            data[k] = item[k]
        else:
            data[k] = None
    data['date'] = _idx
    if idx:=item.get('idx'):
        data['idx'] = idx
    else:
        data['idx'] = f'{_idx}@{item['symbol']}'
    return data

def xue_qiu_hq(item: dict):
    return _(base, item)                                        

def xue_qiu_stock(item: dict):
    return _(stock, item) 

if __name__ == '__main__':
    pass
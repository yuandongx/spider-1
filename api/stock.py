"""
get method
"""
from pymongo import DESCENDING, ASCENDING
from .app import app


def _(item: dict):
    if '_id' in item:
        item['_id'] = str(item['_id'])
    return item



@app.get('/stock/list/{code}/{date}')
async def list_my_follow(code: str, date: str):
    """
    list_item
    """
    _filter = {}
    if code is not None:
        _filter['symbol'] = code
    if date is not None:
        _filter['date'] = date
    rtn = {
        "data": None,
        "count": 0,
        "msg": 'No date found.',
        "status": -1
    }
    if _filter:
        if res := await app.database.myfllows.find_one(_filter):
            rtn['data'] = _(res)
            rtn['count'] = 1
            rtn['msg'] = 'ok'
            rtn['status'] = 0
    return rtn

@app.get('/hq/{node}/{date}')
async def list_hq(node: str, date: str):
    """
    list_hq
    """
    _filter = {}
    if node is not None:
        _filter['node'] = node
    if date is not None:
        _filter['date'] = date
    if _filter:
        data = app.database.hq.find(_filter)
    else:
        data = app.database.hq.find()
    items = [_(item) for item in await data.to_list()]
    rtn = {
        "data": items,
        "count": len(items),
        "msg": 'ok',
        "status": 0
    } 
    return rtn

@app.get('/stock/list')
async def list_stock(prop: str = None, sort: str = None):
    """
    list_stock
    sort: asc, desc
    prop: symbol, name, price, change, percent
    """
    data = app.database.all.find()
    tmp = set()
    items = []
    if sort not in ['asc', 'desc']:
        sort = 'asc'
    
    for item in await data.to_list():
        value = _(item) 
        symbol = value['symbol']
        if symbol not in tmp:
            items.append(value)
            tmp.add(symbol)
        else:
            pass
    if prop not in items[0]:
        prop = 'changepercent'
    items = sorted(items, key=lambda x: str(x[prop]), reverse=True if sort == 'desc' else False)   
    rtn = {
        "data": items,
        "count": len(items),
        "msg": 'ok',
        "status": 0
    } 
    return rtn


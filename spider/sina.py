from loguru import logger
from datetime import datetime

from .fetch.sina import get_hq_node_data as get_sina_hq_data, NODES
from .config import mgdb

def sina_hq():
    """ 
    hs_a
    sz_a
    hs_bjs
    """
    logger.info('【sina_hq】is running...')
    date = datetime.now().strftime('%Y%m%d')
    for node in NODES:
        res = get_sina_hq_data(node)
        payload = {
            "db": "stock",
            "collection": date,
            "data": res['data']
        }
        mgdb.insert_or_update(payload)
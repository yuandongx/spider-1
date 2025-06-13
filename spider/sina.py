from loguru import logger

from .fetch.sina import get_hq_node_data as get_sina_hq_data, NODES
from .config import mgdb

def sina_hq():
    """ 
    hs_a
    sz_a
    hs_bjs
    """
    logger.info('【sina_hq】is running...')

    for node in NODES:
        res = get_sina_hq_data(node)
        payload = {
            "db": "stocks",
            "collection": "daily",
            "data": res['data']
        }
        mgdb.insert_or_update(payload)
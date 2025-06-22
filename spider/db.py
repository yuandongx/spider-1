"""
工厂处理
"""

import os
import re

from urllib.parse import quote_plus
from loguru import logger

from pymongo import MongoClient
from pymongo import UpdateOne, DeleteOne
from pymongo.errors import BulkWriteError

regex = re.compile(r'^\d{8}$')

class Mgdb:
    """
    mongodb
    """
    def __init__(self):
        self.mongo_user = os.getenv('APP_MONGO_USER') or 'root'
        self.mongo_password = os.getenv('APP_MONGO_PASSWORD') or 'example'
        self.mongo_host = os.getenv('APP_MONGO_HOST') or '123.249.37.220'
        self.mongo_port = os.getenv('APP_MONGO_PORT') or 27017
        self.default_db = 'default'
        _user = quote_plus(self.mongo_user)
        _pass = quote_plus(self.mongo_password)
        uri = f"mongodb://{_user}:{_pass}@{self.mongo_host}"
        self.mongodb_client = MongoClient(uri)
        self.database = self._connect()
        

    def _connect(self):
        self.database = self.mongodb_client.get_default_database(
            self.default_db)
        ping_response = self.database.command("ping")
        if int(ping_response["ok"]) != 1:
            raise Exception("Problem connecting to database cluster.")
        else:
            logger.info("Connected to database cluster.")
        return self.database

    def insert_or_update(self, payload):
        """
        更新或插入记录
        """
        db = payload['db']
        collection = payload['collection']
        data = payload['data']
        updates = []
        if len(data) ==0:
            return
        for item in data:
            if _idx := item.get('idx'):
                key = 'idx'
            elif _idx := item.get('股票代码'):
                key = '股票代码'
            else:
                key = None
            if key is not None:
                updates.append(UpdateOne({_idx: key},
                                         {'$set': item},
                                         upsert=True)
                                )
        try:
            res = self.mongodb_client[db][collection].bulk_write(updates)
            return res
        except Exception as e:
            print('--e--->', e)


    def find(self, db, collection, query=None):
        """
        查询数据
        """
        try:
            if query is not None:
                data = self.mongodb_client[db][collection].find(query)
            else:
                data = self.mongodb_client[db][collection].find()
            return list(data)
        except Exception as e:
            print('--find--->', e)
    
    def get_latest_all_stock(self):
        """
        获取最新的所有股票数据
        """
        try:
            # 查询数据
            data = []
            for item in self.mongodb_client['default']['all'].find():
                code = {'idx': item['idx'], 'code': item.get('代码') or item.get('股票代码')}
                data.append(code)
            return data
        except Exception as e:
            print('获取最新的所有股票数据:', e, item)
            return []


    def delete_many(self, data):
        deletes = []
        for item in data['data']:
            one = DeleteOne({'idx': item['idx']})
            deletes.append(one)
        try:
            self.mongodb_client[data['db']][data['collection']].bulk_write(deletes)
            logger.info(f"{data['db']} {data['collection']}")
        except BulkWriteError as bwe:
            logger.error(f'delete_many error: {bwe}')



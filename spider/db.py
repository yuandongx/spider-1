"""
工厂处理
"""

import os
import re

from urllib.parse import quote_plus
from loguru import logger

from pymongo import MongoClient
from pymongo import UpdateOne

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
        self.default_db = 'db'
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
        # print(f'----> {payload}')
        db = payload['db']
        collection = payload['collection']
        data = payload['data']
        updates = []
        if len(data) ==0:
            return
        for item in data:
            _idx = item.get('idx') or item.get('股票代码')
            updates.append(UpdateOne({"idx": _idx}, {
                           '$set': item}, upsert=True))
        try:
            res = self.mongodb_client[db][collection].bulk_write(updates)
            return res
        except Exception as e:
            print('--e--->', e)


    def find(self, db, collection, query):
        """
        查询数据
        """
        try:
            data = self.mongodb_client[db][collection].find(query)
            return list(data)
        except Exception as e:
            print('--e--->', e)
    
    def get_latest_all_stock(self):
        """
        获取最新的所有股票数据
        """
        try:
            # 获取所有集合名称
            collections = self.mongodb_client['realtime'].list_collection_names()
            # 获取最新的集合名称
            latest_collection = sorted(filter(lambda item: regex.match(item), collections))[-1]
            # 查询数据
            data = []
            for item in self.mongodb_client['realtime'][latest_collection].find():
                code = item['idx'].split('@')[1]
                data.append(code)
            return data
        except Exception as e:
            print('--e--->', e)
            return []
        
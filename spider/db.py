"""
工厂处理
"""

import os
from urllib.parse import quote_plus

from loguru import logger


from pymongo import MongoClient
from pymongo import UpdateOne

class Mgdb:
    """
    mongodb
    """
    def __init__(self):
        self.mongo_user = os.getenv('MONGO_USER') or 'root'
        self.mongo_password = os.getenv('MONGO_PASSWORD') or 'example'
        self.mongo_host = os.getenv('MONGO_HOST') or '127.0.0.1'
        self.mongo_port = os.getenv('MONGO_PORT') or 27017
        self.default_db = 'db'
        _user = quote_plus(self.mongo_user)
        _pass = quote_plus(self.mongo_password)
        uri = f"mongodb://{_user}:{_pass}@{self.mongo_host}"
        self.mongodb_client = MongoClient(uri)
        self.database = None

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
        
        for item in data:
            updates.append(UpdateOne({"idx": item['idx']}, {
                           '$set': item}, upsert=True))
        try:
            res = self.mongodb_client[db][collection].bulk_write(updates)
            return res
        except Exception as e:
            print('--e--->', e)



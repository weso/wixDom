__author__ = 'guillermo'
from pymongo import MongoClient


class MongoConnection(object):
    def __init__(self, host, port, db_name):
        self._client = MongoClient(host, port)
        self._db = self._client[db_name]

    @property
    def db(self):
        return self._db






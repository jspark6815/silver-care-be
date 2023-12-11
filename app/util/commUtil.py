import os, sys, json
from pymongo import MongoClient
from pymongo.collation import Collation


with open(os.path.join(sys.path[0], "config.json"), "r", encoding="UTF-8") as configJson:
    config = json.load(configJson)

class CommUtil():
    def __init__(self):
        self.client = MongoClient(host=config['ip'], port=int(config['port']))
        self.db = self.client.silvercare
        self.col_user = self.db.user
        self.col_notice = self.db.notice
        self.col_task = self.db.task

        print(self.db)

    def insert(self, col:Collation, data):
        col.insert_one(data)
    def update(self, col:Collation, origin, data):
        col.update_one(origin, {'$set': data})
    def delete(self, col:Collation, data):
        col.delete_one(data)
    def findOne(self, col:Collation, data):
        return col.find_one(data)
    def findList(self, col:Collation, data):
        return list(col.find(data, {'_id': False}))
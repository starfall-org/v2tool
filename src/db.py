import os
from pymongo import MongoClient


class NoKeyError(Exception):
    pass


class Mongo:
    def __init__(self):
        db_url = os.getenv("MONGO_URL")
        client = MongoClient(db_url)
        db = client.mo9973_notes
        self.notes = db.notes
        self.content = db.content

    def get(self, note):
        result = self.notes.find_one({"_id": note})

        if result:
            return result["urls"]
        else:
            raise NoKeyError("Không tìm thấy dữ liệu")

    def add_value(self, key, content):
        self.content.update_one({"_id": key}, {"$set": {"value": content}}, upsert=True)

    def get_value(self, key):
        result = self.content.find_one({"_id": key})

        if result:
            return result["value"]
        else:
            raise NoKeyError("Không tìm thấy dữ liệu")


def get_data(note):
    db_url = os.getenv("MONGO_URL")
    client = MongoClient(db_url)
    db = client.mo9973_notes
    notes = db.notes
    result = notes.find_one({"_id": note})
    return result["urls"]

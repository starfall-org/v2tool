import os
from pymongo import MongoClient

class Mongo:
    def __init__(self):
        db_url = os.getenv("MONGO_URL")
        client = MongoClient(db_url)
        db = client.mo9973_notes
        self.notes = db.notes

    def get(self, note):
        result = self.notes.find_one({"id": note})
        
        if result:
            return result.get('urls')
        else:
            raise Exception("Không tìm thấy dữ liệu") 

def get_data(note):
    db_url = os.getenv("MONGO_URL")
    client = MongoClient(db_url)
    db = client.mo9973_notes
    notes = db.notes
    result = notes.find_one({"_id": note})
    return result["urls"]
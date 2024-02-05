from deta import Deta
import os

deta = Deta(os.getenv('DETA_KEY'))
db = deta.Base("notes")

class Proxy:
    @staticmethod
    def set(config):
        db.put(key="proxy", data=config)
        return "DONE"
    def get():
        

def get_data(filename):
    entry = db.get(filename)
    if entry:
        return entry['urls']
    else:
        raise Exception("Không tìm thấy dữ liệu")
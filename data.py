from deta import Deta
import os

deta = Deta(os.getenv('DETA_KEY'))
db = deta.Base("notes")

class Proxy:
    @staticmethod
    def set(config):
        db.put(key="proxy", data=config)
        return "OK"
        
    @staticmethod
    def get():
        config = db.get("proxy")["value"]
        proxy = "http://127.0.0.1:8888"
        os.system(f"./lite -p 8888 {config}")
        os.environ["http_proxy"]=proxy
        os.environ["https_proxy"]=proxy
        return "OK"

def get_data(filename):
    entry = db.get(filename)
    if entry:
        return entry['urls']
    else:
        raise Exception("Không tìm thấy dữ liệu")
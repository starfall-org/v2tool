from deta import Deta
from threading import Thread
import requests
import os

deta = Deta(os.getenv('DETA_KEY'))
db = deta.Base("notes")
proxy = "http://127.0.0.1:8888"

class Proxy:
    @staticmethod
    def add(config):
        db.put(key="proxy", data=config)
        os.system(f"./lite -p 8888 {config} &")
        os.environ["http_proxy"]=proxy
        os.environ["https_proxy"]=proxy
        try:
            r = requests.get("https://www.google.com/generate_204")
            if r.status_code != 204:
                raise
        except Exception as e:
            print(e)
            del os.environ["http_proxy"]
            del os.environ["https_proxy"]
            return False
        return True
        
    @staticmethod
    def run():
        config = db.get("proxy")["value"]
        os.system(f"./lite -p 8888 {config} &")
        os.environ["http_proxy"]=proxy
        os.environ["https_proxy"]=proxy
        try:
            r = requests.get("https://www.google.com/generate_204")
            if r.status_code != 204:
                raise
        except Exception as e:
            print(e)
            del os.environ["http_proxy"]
            del os.environ["https_proxy"]
            return False
        return True

def get_data(filename):
    entry = db.get(filename)
    if entry:
        return entry['urls']
    else:
        raise Exception("Không tìm thấy dữ liệu")
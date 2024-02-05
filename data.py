from deta import Deta
from threading import Thread
import requests
import os
import time

deta = Deta(os.getenv('DETA_KEY'))
db = deta.Base("notes")
proxy = "http://127.0.0.1:8888"
expath = os.path.abspath(__file__).replace("/data.py", "")

def test_proxy():
    start_time = time.time()
    while True:
        if time.time() - start_time >= 6:
            del os.environ["http_proxy"]
            del os.environ["https_proxy"]
            return False
        try:
            requests.get("https://www.google.com/generate_204")
            return True
        except Exception:
            continue
       
class Proxy:
    @staticmethod
    def add(config):
        db.put(key="proxy", data=config)
        os.system(f"{expath}/lite -p 8888 {config} &")
        os.environ["http_proxy"]=proxy
        os.environ["https_proxy"]=proxy
        return test_proxy()
        
    @staticmethod
    def run():
        config = db.get("proxy")["value"]
        os.system(f"{expath}/lite -p 8888 {config} &")
        os.environ["http_proxy"]=proxy
        os.environ["https_proxy"]=proxy
        return test_proxy()

def get_data(filename):
    entry = db.get(filename)
    if entry:
        return entry['urls']
    else:
        raise Exception("Không tìm thấy dữ liệu")
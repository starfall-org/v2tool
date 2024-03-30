from deta import Deta
from threading import Thread
import requests
import os
import time

deta = Deta(os.getenv('DETA_KEY'))
db = deta.Base("notes")
local_proxy = "http://127.0.0.1:10808"
proxies = {
    "http": local_proxy,
    "https": local_proxy
    }
proxy_url = os.getenv('PROXY_URL')
r = requests.get(proxy_url)
config = r.text

def test_proxy():
    start_time = time.time()
    while True:
        if time.time() - start_time >= 3:
            return False
        try:
            requests.get(
                "https://www.google.com/generate_204", 
                timeout=1, 
                proxies=proxies
                )
            return True
        except Exception:
            continue

class Proxy:
    @staticmethod
    def add():
        os.system(f"./lite -p 10808 {config} &")
        return test_proxy()
        
    @staticmethod
    def run():
        os.system(f"./lite -p 10808 {config} &")
        return test_proxy()

def get_data(filename):
    entry = db.get(filename)
    if entry:
        return entry['urls']
    else:
        raise Exception("Không tìm thấy dữ liệu")
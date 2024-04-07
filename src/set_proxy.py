import os
import requests
import time


local_proxy = "http://127.0.0.1:10808"
proxies = {
    "http": local_proxy,
    "https": local_proxy
    }
proxy_url = os.getenv('PROXY_URL')

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

def run_proxy():
    r = requests.get(proxy_url)
    config = r.text
    os.system(f"./lite -p 10808 {config} &")
    return test_proxy()
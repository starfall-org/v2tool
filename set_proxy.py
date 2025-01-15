import os
import time
import requests

local_proxy = "http://127.0.0.1:2002"
proxies = {"http": local_proxy, "https": local_proxy}
proxy_url = os.getenv("PROXY_URL")


def test_proxy():
    start_time = time.time()
    while True:
        if time.time() - start_time >= 3:
            return False
        try:
            requests.get(
                "https://www.google.com/generate_204", timeout=1, proxies=proxies
            )
            return True
        except Exception:
            continue


def run_proxy():
    r = requests.get(proxy_url)
    config = r.text
    os.system("pkill -9 lite")
    os.system(f"./lite -p 2002 {config} &")
    return test_proxy()

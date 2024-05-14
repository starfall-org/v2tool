import os
import requests

local_proxy = "http://127.0.0.1:10808"
proxies = {"http": local_proxy, "https": local_proxy}
proxy_url = os.getenv("PROXY_URL")


def test_proxy():
    req = requests.get(
        "https://www.google.com/generate_204", timeout=2, proxies=proxies
    )
    return req.status_code


def run_proxy():
    r = requests.get(proxy_url)
    config = r.text
    os.system(f"./lite -p 10808 {config} &")
    return test_proxy()

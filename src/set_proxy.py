import os
import requests

proxy_url = os.getenv("PROXY_URL")
proxy_addr = os.getenv("HTTP", "http://127.0.0.1:10808")
proxies = {"http": proxy_addr, "https": proxy_addr}


def run_proxy():
    r = requests.get(proxy_url)
    config = r.text
    os.system(f"./lite -p 10808 {config} &")
    return "OK"


def set_proxy(config):
    os.system(f"./lite -p 10808 {config} &")
    return "OK"

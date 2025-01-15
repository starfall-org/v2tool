import socket
import requests


def get_loc(addr: str = "www.google.com"):
    host = socket.gethostbyaddr(addr)
    ip = host[2][0]
    req = requests.get(f"https://ipinfo.io/{ip}", timeout=99)
    res = req.json()
    city = res.get("city")
    country = res.get("country")
    org = res.get("org")
    if org:
        org = " ".join(org.split(" ")[1:])
    tag = [f"[{org}]", city, country]
    return " ".join(tag)

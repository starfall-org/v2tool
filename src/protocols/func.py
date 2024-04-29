import socket
import requests


def get_loc(addr: str = "www.google.com"):
    host = socket.gethostbyaddr(addr)
    req = requests.get(f"https://ipinfo.io/{host}")
    res = req.json()
    city = res.get("city")
    country = res.get("country")
    org = res.get("org")
    if org:
        org = " ".join(org.split(" ")[1:])
    tag = [org.upper(), city, country]
    return " ".join(tag)

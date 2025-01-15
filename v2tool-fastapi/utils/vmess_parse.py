import base64
import json



def vmess(link: str, set_uuid: str, set_sni: str, set_tag: str) -> tuple:
    code = link.split("://")[1]
    config = base64.b64decode(code).decode("utf-8")
    config = json.loads(config)
    netloc = config["id"] + "@" + config["add"] + ":" + str(config["port"])
    ip = config["add"]
    net = config["net"]
    if ip in ["127.0.0.1", "1.1.1.1", "0.0.0.0", "8.8.8.8"]:
        return
    if set_tag:
        config["ps"] = set_tag
    if set_uuid:
        config["id"] = set_uuid
    if set_sni:
        if net == "tcp":
            config["sni"] = set_sni
        else:
            config["host"] = set_sni
    config = json.dumps(config).encode("utf-8")
    code = base64.b64encode(config).decode("utf-8")
    link = f"vmess://{code}"
    return link, netloc

from .vmess_parse import vmess
from .trojan_parse import trojan
from .vless_parse import vless


def processes(links: list, uuid: str = None, sni: str = None, tag: str = None) -> list:
    duplicate = []
    results = []
    for link in links:
        try:
            result = None
            if link.startswith("vmess://"):
                result = vmess(link, uuid, sni, tag)
            elif link.startswith("trojan://"):
                result = trojan(link, uuid, sni, tag)
            elif link.startswith("vless://"):
                result = vless(link, uuid, sni, tag)
            else:
                results.append(link)
        except Exception as e:
            print(e)
            continue
        if result and result[1] not in duplicate:
            results.append(result[0])
            duplicate.append(result[1])
    return results

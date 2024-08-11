from .protocols import trojan, vless, vmess


def processes(links: list, uuid: str = None, sni: str = None, tag: str = None):
    duplicate = []
    results = []
    for link in links:
        if link.startswith("vmess"):
            result = vmess.edit(link, uuid, sni, tag)
        elif link.startswith("trojan"):
            result = trojan.edit(link, uuid, sni, tag)
        elif link.startswith("vless"):
            result = vless.edit(link, uuid, sni, tag)
        else:
            results.append(link)
        if result and isinstance(result, tuple) and len(result) == 2:
            if result[1] not in duplicate:
                results.append(result[0])
                duplicate.append(result[1])
    return results

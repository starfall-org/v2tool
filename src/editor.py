from .protocols import trojan, vless, vmess


def editor(
    links: list, values: set, uuid: str = None, sni: str = None, tag: str = None
):
    for link in links:
        if link.startswith("vmess"):
            link = vmess.edit(link, uuid, sni, tag)
        elif link.startswith("trojan"):
            link = trojan.edit(link, uuid, sni, tag)
        elif link.startswith("vless"):
            link = vless.edit(link, uuid, sni, tag)
        if link:
            values.add(link)


def processes(links: list, uuid: str = None, sni: str = None, tag: str = None):
    values = set()
    duplicate = []
    result = []
    editor(links, values, uuid, sni, tag)
    for value in values:
        if value[1] not in duplicate:
            result.append(value[0])
            duplicate.append(value[1])
    return result

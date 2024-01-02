import re

def edit(link, set_uuid=None, set_sni=None, set_tag=None):
    link = link.split('://')[1]
    uuid = link.split('@')[0]
    ip, port = link.split('@')[1].split('?')[0].split(':')

    if port == 443:
        sni, tag = re.search(r'sni=([^&]+)&.*#(.+)', link).groups()
    else:
        sni = re.search(r'host=([^&]+)&.*#(.+)', link).group(1)
        tag = re.search(r'#(.+)', link).group(1)

    if ip in ['127.0.0.1', '1.1.1.1', '0.0.0.0', '8.8.8.8']:
        return

    if set_uuid:
        link = link.replace(uuid, set_uuid)
    if set_sni:
        link = link.replace(sni, set_sni)
    if set_tag:
        link = link.replace(tag, set_tag)

    full_link = f"vless://{link}"
    return full_link
import re
#vless://7de1b798-fa3e-4029-b3f6-62959c1d6c0b@ngiandzang.nguyendinhnghi.id.vn:443?type=tcp&security=tls&fp=&alpn=h2%2Chttp%2F1.1%2Ch3&allowInsecure=1&sni=dl.kgvn.garenanow.com#3%09%09%09%F0%9F%8D%80Nguy%E1%BB%85n%20Ngi%20And%20Nguy%E1%BB%85n%20Zang%F0%9F%92%96%20Vless%20Tls%20Hyper%20NetWork%E2%84%A2%EF%B8%8F-owngxk57

def edit(link, set_uuid, set_sni, set_tag):
  link = link.split('://')[1]
  uuid = link.split('@')[0]
  ip, port = link.split('@')[1].split('?')[0].split(':')
  if port == 443:
    sni = link.split('sni=')[1].split('#')[0]
    tag = link.split('#')[-1]
  else:
    sni = link.split('host=')[1].split('&')[0]
    tag = re.search(r'#(.+)', link).group(1)
  if ip in ['127.0.0.1', '1.1.1.1', '0.0.0.0', '8.8.8.8']:
    return
  if set_uuid:
    link = link.replace(uuid, set_uuid)
  if set_sni:
    link = link.replace(sni, set_sni)
  if set_tag:
    link = link.replace(tag, set_tag)
  else:
    link = link.replace(tag, tag)
  full_link = f"vless://{link}"
  return full_link
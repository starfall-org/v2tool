edited = []
num = 0
#link = trojan://uuid@0.0.0.0:443?security=tls&headerType=none&type=tcp&sni=sni.com#Name
def edit(link, set_uuid=None, set_sni=None, set_tag=None):
  global edited, num
  link = link.split('://')[1]
  uuid = link.split('@')[0]
  ip, port = link.split('?')[0].split('@')[1].split(':')
  sni, tag = link.split('sni=')[1].split('#')
  key = { f'{ip}:{port}' : uuid }
  if ip in ['127.0.0.1', '1.1.1.1', '0.0.0.0', '8.8.8.8'] or key in edited:
    return
  if set_uuid:
    link = link.replace(uuid, set_uuid)
  if set_sni:
    link = link.replace(sni, set_sni)
  if set_tag:
    set_tag = f'{set_tag} trojan{num}'
    link = link.replace(tag, set_tag)
  full_link = f"trojan://{link}"
  return full_link
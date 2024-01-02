import re
import base64
import json

def edit(link, set_uuid=None, set_sni=None, set_tag=None):
  global edited, num
  code = link.split("://")[1]
  config = base64.b64decode(code).decode('utf-8')
  config = json.loads(config)
  ip = config["add"]
  tag = config['ps']
  uuid = config['id']
  sni = config['sni']
  host = config['host']
  port = config['port']
  key = { f'{ip}:{port}' : uuid }
  if ip in ['127.0.0.1', '1.1.1.1', '0.0.0.0', '8.8.8.8']:
    return
  if set_tag:
    tag = str(set_tag)
  if set_uuid:
    uuid = set_uuid
  if set_sni:
    if port == 80:
      host = set_sni
    elif port == 443:
      sni = set_sni
    else:
      host = sni = set_sni
  num += 1
  config = json.dumps(config).encode('utf-8')
  code = base64.b64encode(config).decode('utf-8')
  link = f"vmess://{code}"
  return link, key
from configkit import vmess, trojan, vless

def editor(link, uuid=None, sni=None, tag=None):
  if link.startswith('vmess'):
    value = vmess.edit(link, uuid, sni, tag)
  elif link.startswith('trojan'):
    value = trojan.edit(link, uuid, sni, tag)
  elif link.startswith('vless'):
    value = vless.edit(link, uuid, sni, tag)
  else:
    value = link
  return value
  
def add_link(batch, uuid, sni, tag, values):
  for link in batch:
    value = editor(link, uuid, sni, tag)
    values.add(value)
  
def processes(links, uuid=None, sni=None, tag=None):
  batch_size = 1
  values = set()
  for i in range(0, len(links), batch_size):
    batch = links[i:i + batch_size]
    add_link(batch, uuid, sni, tag, values)
  return list(values)
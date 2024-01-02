from configkit import vmess, trojan, vless

def editor(batch, values, uuid=None, sni=None, tag=None):
  for link in batch:
    if link.startswith('vmess'):
      value = vmess.edit(link, uuid, sni, tag)
    elif link.startswith('trojan'):
      value = trojan.edit(link, uuid, sni, tag)
    elif link.startswith('vless'):
      value = vless.edit(link, uuid, sni, tag)
    else:
      value = link
    values.add(value)
  
def processes(links, uuid=None, sni=None, tag=None):
  batch_size = 1
  values = set()
  for i in range(0, len(links), batch_size):
    batch = links[i:i + batch_size]
    editor(batch, values, uuid, sni, tag)
  return list(values)
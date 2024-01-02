from configkit import vmess, trojan, vless

def editor(batch, uuid=None, sni=None, tag=None):
  values = []
  for link in batch:
    if link.startswith('vmess'):
      value = vmess.edit(link, uuid, sni, tag)
    elif link.startswith('trojan'):
      value = trojan.edit(link, uuid, sni, tag)
    elif link.startswith('vless'):
      value = vless.edit(link, uuid, sni, tag)
    else:
      value = link
    values.append(value)
  return values
  
def processes(links, uuid=None, sni=None, tag=None):
  batch_size = 1
  values = []
  for i in range(0, len(links), batch_size):
    batch = links[i:i + batch_size]
    value = editor(batch, values, uuid, sni, tag)
    values.extend(value)
  return values
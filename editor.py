from configkit import vmess, trojan, vless

def editor(batch, uuid=None, sni=None, tag=None):
  links = []
  for link in batch:
    if link.startswith('vmess'):
      link = vmess.edit(link, uuid, sni, tag)
    elif link.startswith('trojan'):
      link = trojan.edit(link, uuid, sni, tag)
    elif link.startswith('vless'):
      link = vless.edit(link, uuid, sni, tag)
    links.append(link)
  return links
  
def processes(links, uuid=None, sni=None, tag=None):
  batch_size = 1
  values = []
  for i in range(0, len(links), batch_size):
    batch = links[i:i + batch_size]
    value = editor(batch, values, uuid, sni, tag)
    values.extend(value)
  return values
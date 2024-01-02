from configkit import vmess, trojan, vless
import concurrent.futures

def editor(batch, values, uuid=None, sni=None, tag=None):
  links = []
  for link in batch:
    if link.startswith('vmess'):
      link, key = vmess.edit(link, uuid, sni, tag)
    elif link.startswith('trojan'):
      link, key = trojan.edit(link, uuid, sni, tag)
    elif link.startswith('vless'):
      link, key = vless.edit(link, uuid, sni, tag)
    values.add(link)
   # links.append(link)
    #keys.append(key)
  return links
  
def _processes(links, uuid=None, sni=None, tag=None):
  batch_size = 10
  values = []
  for i in range(0, len(links), batch_size):
    batch = links[i:i + batch_size]
    value = editor(batch, uuid, sni, tag)
    values.extend(value)
  return values
  
def processes(links, uuid=None, sni=None, tag=None):
  batch_size = 10
  values = set()
  keys = []
  def process_batch(batch):
    try:
      value = editor(batch, values, uuid, sni, tag)
      #values.extend(value)
    except Exception as e:
      pass
  with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(process_batch, (links[i:i + batch_size] for i in range(0, len(links), batch_size)))
  return list(values)
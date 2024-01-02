from configkit import vmess, trojan, vless
import concurrent.futures

def editor(batch, values, keys, uuid=None, sni=None, tag=None):
  for link in batch:
    if link.startswith('vmess'):
      link, key = vmess.edit(link, uuid, sni, tag)
    elif link.startswith('trojan'):
      link, key = trojan.edit(link, uuid, sni, tag)
    elif link.startswith('vless'):
      link, key = vless.edit(link, uuid, sni, tag)
    #if key in list(keys):
     # continue
    values.add(link)
    keys.add(key)
  return links
  
# def _processes(links, uuid=None, sni=None, tag=None):
#   batch_size = 10
#   values = []
#   for i in range(0, len(links), batch_size):
#     batch = links[i:i + batch_size]
#     value = editor(batch, uuid, sni, tag)
#     values.extend(value)
#   return values
  
def processes(links, uuid=None, sni=None, tag=None):
  batch_size = 10
  values = set()
  keys = set()
  def process_batch(batch):
    try:
      value = editor(batch, values, keys, uuid, sni, tag)
    except Exception as e:
      pass
  with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(process_batch, (links[i:i + batch_size] for i in range(0, len(links), batch_size)))
  return list(values)
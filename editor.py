from configkit import vmess, trojan, vless
import concurrent.futures

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
  batch_size = 10
  values = []
  for i in range(0, len(links), batch_size):
    batch = links[i:i + batch_size]
    value = editor(batch, uuid, sni, tag)
    values.extend(value)
  return values
  
def _processes(links, uuid=None, sni=None, tag=None):
  batch_size = 10
  values = []
  def process_batch(batch):
    try:
      return editor(batch, uuid, sni, tag)
    except Exception as e:
      print(f"Error processing batch {batch}: {e}")
      return []
  with concurrent.futures.ThreadPoolExecutor() as executor:
    values = list(executor.map(process_batch, (links[i:i + batch_size] for i in range(0, len(links), batch_size))))
  return values
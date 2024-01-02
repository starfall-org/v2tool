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
  
# def processes(links, uuid=None, sni=None, tag=None):
#   batch_size = 1
#   values = []
#   for i in range(0, len(links), batch_size):
#     batch = links[i:i + batch_size]
#     value = editor(batch, uuid, sni, tag)
#     values.extend(value)
#   return values
  
def processes(links, uuid=None, sni=None, tag=None):
    batch_size = 1
    values = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(editor, batch, uuid, sni, tag): batch for batch in (links[i:i + batch_size] for i in range(0, len(links), batch_size))}
        
        for future in concurrent.futures.as_completed(futures):
            batch = futures[future]
            try:
                value = future.result()
                values.extend(value)
            except Exception as e:
                # Handle exceptions raised in the editor function
                print(f"Error processing batch {batch}: {e}")

    return values
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def edit(link, set_uuid, set_sni, set_tag):
  link = urlparse(link)
  query = parse_qs(link.query)
  netloc = link.netloc.split('@')
  ip = netloc[1].split(':')[0]
  if ip in ['127.0.0.1', '1.1.1.1', '0.0.0.0', '8.8.8.8']:
    return
  if set_uuid:
    netloc[0] = set_uuid
    netloc = "@".join(netloc)
    link = link._replace(netloc=netloc)
  if set_sni:
    if query['type'] == 'tcp':
      query['sni'] = [set_sni]
    else:
      query['host'] = [set_sni]
    query = urlencode(query, doseq=True)
    link = link._replace(query=query)
  if set_tag:
    link = link._replace(fragment=set_tag)
  link = urlunparse(link)
  return link
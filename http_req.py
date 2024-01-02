import base64
import json
import requests
import re
import concurrent.futures
from data import workers

def get_response(url):
    response = requests.get(url, headers={"User-Agent": "v2rayNG/1.8.12"})
    if response.status_code == 200:
      response = response.text
    else:
      response = requests.get(workers, params={"url": query_url}).text
    links = []
    if any(proto in response for proto in ["vmess:", "trojan:", "vless:"]):
      for link in response.splitlines():
        if any(proto in link for proto in ["vmess:", "trojan:", "vless:"]):
          links.append(link)
    elif any(proto in response for proto in ["http:", "https:"]):
      url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
      sub_urls = re.findall(url_pattern, response)
      links = get_responses(sub_urls)
    else:
      try:
        decoded_line = base64.b64decode(response).decode('utf-8')
        for link in decoded_line.splitlines():
          if any(proto in link for proto in ["vmess:", "trojan:", "vless:"]):
            links.append(link)
      except:
        links = []
    return links
    
def get_responses(urls):
  list_links = []
  with concurrent.futures.ThreadPoolExecutor() as executor:
    links = executor.map(process, urls)
    list_links.extend(links)
  return list_links
    
def process(url):
  links = []
  sub_response = requests.get(url, timeout=5, headers={"User-Agent": "v2rayNG/1.8.12"})
  if sub_response.status_code == 200:
    sub_response = sub_response.text
  else:
    sub_response = requests.get(workers, params={"url": url}, timeout=5)
  if any(proto in sub_response for proto in ["vmess:", "trojan:", "vless:"]):
    links.extend(sub_response.splitlines())
  elif sub_response is None:
    return []
  else:
    decoded_line = base64.b64decode(sub_response).decode('utf-8')
    if any(proto in decoded_line for proto in ["vmess:", "trojan:", "vless:"]):
      links.extend(decoded_line.splitlines())
  return links
    
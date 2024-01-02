import base64
import json
import requests
import re
import concurrent.futures

def get_response(url):
    response = requests.get(url, headers={"User-Agent": "v2rayNG/1.8.12"}).text
    links = []
    if any(proto in response for proto in ["vmess:", "trojan:", "vless:"]):
      for link in response.splitlines():
        if any(proto in link for proto in ["vmess:", "trojan:", "vless:"]):
          links.append(link)
    elif any(proto in response for proto in ["http:", "https:"]):
      url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
      sub_urls = re.findall(url_pattern, response)
      links = sub_response(sub_urls)
    else:
      try:
        decoded_line = base64.b64decode(response).decode('utf-8')
        for link in decoded_line.splitlines():
          if any(proto in link for proto in ["vmess:", "trojan:", "vless:"]):
            links.append(link)
      except:
        links = []
    return links
    
def sub_response(urls):
  with concurrent.futures.ThreadPoolExecutor() as executor:
    links = executor.map(process, urls)
    return links
    
def process(url):
  links = []
  sub_response = requests.get(url, timeout=10, headers={"User-Agent": "v2rayNG/1.8.12"}).text
  if any(proto in sub_response for proto in ["vmess:", "trojan:", "vless:"]):
    links.extend(sub_response.splitlines())
  else:
    decoded_line = base64.b64decode(sub_response).decode('utf-8')
    if any(proto in decoded_line for proto in ["vmess:", "trojan:", "vless:"]):
      links.extend(decoded_line.splitlines())
  return links
    
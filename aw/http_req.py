import base64
import json
import requests
import re
import concurrent.futures
from ..data import workers, proxy

def get_response(url):
    try:
        response = requests.get(url, timeout=3, headers={"User-Agent": "v2rayNG/1.8.12"})
        if response.status_code != 200:
            raise
        response = response.text
    except:
        try:
            response = requests.get(proxy, params={"url": url}, timeout=3).text
        except:
            response = requests.get(workers, params={"url": url}, timeout=3).text
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
        decoded_line = base64.b64decode(response).decode('utf-8')
        for link in decoded_line.splitlines():
          if any(proto in link for proto in ["vmess:", "trojan:", "vless:"]):
            links.append(link)
    return links
    
def get_responses(urls):
  links = []
  def process(url):
    try:
      sub_response = requests.get(url, timeout=3, headers={"User-Agent": "v2rayNG/1.8.12"})
      if sub_response.status_code != 200:
        raise
      sub_response = sub_response.text
    except:
      try:
          sub_response = requests.get(proxy, params={"url": url}, timeout=3).text
      except:
          sub_response = requests.get(workers, params={"url": url}, timeout=3).text
    if any(proto in sub_response for proto in ["vmess:", "trojan:", "vless:"]):
      links.extend(sub_response.splitlines())
    else:
      try:
        decoded_line = base64.b64decode(sub_response).decode('utf-8')
        if any(proto in decoded_line for proto in ["vmess:", "trojan:", "vless:"]):
          links.extend(decoded_line.splitlines())
      except:
        pass
  with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(process, urls)
  return links
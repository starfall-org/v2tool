import base64
import json
import requests
import re
import pycurl
import concurrent.futures
from io import BytesIO
from ..data import workers, proxy

def get_response(url):
    response = requests.get(url, timeout=3, headers={"User-Agent": "v2rayNG/1.8.12"})
    if response.status_code == 200:
      response = response.text
    else:
      response = requests.get(workers, params={"url": query_url}, timeout=5).text
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
        pass
    return links

def get_responses(urls):
  links = []
  def process(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    try:
      c.setopt(c.URL, url)
      c.setopt(c.USERAGENT, 'v2rayNG/1.8.12')
      c.setopt(c.CONNECTTIMEOUT, 3)
      c.setopt(c.WRITEDATA, buffer)
      c.perform()
      c.close()
      status_code = c.getinfo(pycurl.HTTP_CODE)
      body = buffer.getvalue()
      if status_code != 200:
        raise
      sub_response = body.decode('utf-8')
    except:
      try:
          c.setopt(c.URL, proxy)
          c.setopt(c.POSTFIELDS, f"url={url}")
          c.setopt(c.CONNECTTIMEOUT, 3)
          c.setopt(c.WRITEDATA, buffer)
          c.perform()
          c.close()
          sub_response = requests.get(proxy, params={"url": url}, timeout=5).text
      except:
          c.setopt(c.URL, workers)
          c.setopt(c.POSTFIELDS, f"url={url}")
          c.setopt(c.CONNECTTIMEOUT, 3)
          c.setopt(c.WRITEDATA, buffer)
          c.perform()
          c.close()
    sub_response = buffer.getvalue().decode('utf-8')
    if any(proto in sub_response for proto in ["vmess:", "trojan:", "vless:"]):
      links.extend(sub_response.splitlines())
    else:
      try:
        decoded_line = base64.b64decode(sub_response).decode('utf-8')
        if any(proto in decoded_line for proto in ["vmess:", "trojan:", "vless:"]):
          links.extend(decoded_line.splitlines())
      except:
        pass
  with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(process, urls)
  return links

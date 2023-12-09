from .utils import get_links_from_response, get_links_from_http, get_links_from_https, process_links, process_multi
import requests, base64, os
from deta import Deta

workers = os.getenv('WORKERS')

deta = Deta(os.environ.get('DETA_KEY'))
db = deta.Base("v2ray-notes")

def main(context):
  if context.req.path == "/":
    return process_query(context)
  elif context.req.path.startswith("/list/"):
    return get_all_urls(context)
  elif "get" in context.req.path:
    return process_all_config(context)
  else:
    return "Đường dẫn không hợp lệ."
def get_all(filename):
    existing_entry = db.get(filename)
    if existing_entry:
        urls = existing_entry['urls']
        return urls
    else:
        raise DatabaseNotFoundError("Không tìm thấy dữ liệu")
        
def process_query(context):
    try:
      query_url = context.req.query['url']
    except:
      query_url = None
    if not query_url:
        return "Vui lòng cung cấp tham số URL", 200
    try:
      uuid = context.req.query['uuid']
    except:
      uuid = None
    try:
      sni = context.req.query['sni']
    except:
      sni = None
    try:
      proxy = context.req.query['proxy']
    except:
      proxy = None
    try:
      func = context.req.query['function']
    except:
      func = None
    try:
     ua = context.req.query['ua']
    except:
      ua = "v2rayNG/1.8.12"
    headers = {"User-Agent": ua, "Accept-Encoding": "gzip"}
    if proxy == "true":
      response = requests.get(workers, timeout=5, headers=headers, params={"url": query_url}).text
    else:
      response = requests.get(query_url, timeout=5, headers=headers, params={"flag":"v2rayn"}).text
    links = get_links_from_response(response)
    if not links:
        links = get_links_from_https(response, headers, proxy)
    if func == "single":
      final_links = process_links(links, uuid, sni)
    else:
      final_links = process_multi(links, uuid, sni)
    result = '\n'.join(final_links)
    encoded_result = base64.b64encode(result.encode('utf-8')).decode('utf-8')
    return encoded_result
    
def get_all_urls(context):
    try:
      req_path = context.req.path
      filename = req_path.replace("/list/", "")
      urls = get_all(filename)
      resp = '\n'.join(urls)
      return resp
    except:
      return {"status": "failed", "message": "kho luu tru khong ton tai"}
      
def process_all_config(context):
    req_path = context.req.path
    filename = req_path.replace("/get/", "")
    try:
      uuid = context.req.query['uuid']
    except:
      uuid = None
    try:
      sni = context.req.query['sni']
    except:
      sni = None
    try:
      proxy = context.req.query['proxy']
    except:
      proxy = None
    try:
      func = context.req.query['function']
    except:
      func = None
    try:
      ua = context.req.query['ua']
    except:
      ua = "v2rayNG/1.8.12"
    headers = {"User-Agent": ua, "Accept-Encoding": "gzip"}
    try:
      urls_json = get_all(filename) 
      urls = '\n'.join(urls_json) 
    except:
      return {"status": "failed", "message": "kho luu tru khong ton tai"}
    if func != "single":
      links = get_links_from_https(urls,headers, proxy)
    else:
      links = get_links_from_http(url, headers)
    final_links = process_multi(links, uuid, sni)
    result = '\n'.join(final_links)
    encoded_result = base64.b64encode(result.encode('utf-8')).decode('utf-8')
    return encoded_result
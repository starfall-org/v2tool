from .aw.http_req import get_response, get_responses
from .aw.editor import processes
from .data import get_data
from urllib.parse import unquote
import base64

def main(context):
  if context.req.path == "/":
    return context.res.send(process_query(context))
  elif context.req.path.startswith("/list/"):
    return context.res.send(get_all_urls(context))
  elif "get" in context.req.path:
    return context.res.send(process_all_config(context))
  else:
    return context.res.send("Đường dẫn không hợp lệ.")
        
def process_query(context):
    try:
      query_url = context.req.query['url']
    except:
      query_url = None
    if not query_url:
        return "Vui lòng cung cấp tham số URL"
    try:
      uuid = context.req.query['uuid']
    except:
      uuid = None
    try:
      sni = context.req.query['sni']
    except:
      sni = None
    try:
      tag = context.req.query['tag']
    except:
      tag = None
    query_url = unquote(query_url)
    list_links = get_response(query_url)
    links = processes(list_links, uuid, sni, tag)
    links = '\n'.join(links).encode('utf-8')
    result = base64.b64encode(links).decode('utf-8')
    return result
    
def get_all_urls(context):
    try:
      req_path = context.req.path
      filename = req_path.replace("/list/", "")
      urls = get_data(filename)
      resp = '\n'.join(urls)
      return resp
    except:
      return "Kho lưu trữ không tồn tại"
      
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
    tag = context.req.query['tag']
  except:
    tag = None
  try:
    urls = get_data(filename)
  except Exception as e:
    return str(e)
  list_links = get_responses(urls)
  links = processes(list_links, uuid, sni, tag)
  links = '\n'.join(links).encode('utf-8')
  result = base64.b64encode(links).decode('utf-8')
  return result
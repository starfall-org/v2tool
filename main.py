from .http_req import get_response, get_responses
from .editor import processes
from .data import get_data, Proxy
from urllib.parse import unquote
import base64

def main(context):
    if not context.req.path.startswith("/proxy"):
        try:
            Proxy.run()
        except Exception as e:
            print(e)
            pass
    if context.req.path == "/":
        return context.res.send(process_query(context))
    elif context.req.path.startswith("/get"):
        return context.res.send(process_all_config(context))
    elif context.req.path.startswith("/proxy"):
        config = context.req.query.get("add")
        if config:
            init = Proxy.add(config)
            if init:
                return context.res.send("Thiết lập hoàn tất")
            else:
                return context.res.send("Proxy bị lỗi")
        else:
            return context.res.send("Vui lòng cung cấp link proxy")
    else:
        return context.res.send("Đường dẫn không hợp lệ.")
        
def process_query(context):
        query_url = context.req.query.get('url')
        if not query_url:
            return "Vui lòng cung cấp tham số URL"
        uuid = context.req.query.get('uuid')
        sni = context.req.query.get('sni')
        tag = context.req.query.get('tag')
        query_url = unquote(query_url)
        list_links = get_response(query_url)
        links = processes(list_links, uuid, sni, tag)
        links = '\n'.join(links).encode('utf-8')
        result = base64.b64encode(links).decode('utf-8')
        return result
      
def process_all_config(context):
    req_path = context.req.path
    filename = req_path.replace("/get/", "")
    uuid = context.req.query.get('uuid')
    sni = context.req.query.get('sni')
    tag = context.req.query.get('tag')
    try:
        urls = get_data(filename)
    except Exception as e:
        return str(e)
    list_links = get_responses(urls)
    links = processes(list_links, uuid, sni, tag)
    links = '\n'.join(links).encode('utf-8')
    result = base64.b64encode(links).decode('utf-8')
    return result
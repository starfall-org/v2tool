from flask import Flask, request, Response, render_template, make_response
from utils import get_links_from_response, get_links_from_http, get_links_from_https, process_links, process_multi
import requests, base64, os
from deta import Deta
from utils import workers

app = Flask(__name__)
workers = os.getenv('WORKERS')

deta = Deta(os.environ.get('DETA_KEY'))
db = deta.Base("v2ray-notes")

def get_all(filename):
    existing_entry = db.get(filename)
    if existing_entry:
        urls = existing_entry['urls']
        return urls
    else:
        raise DatabaseNotFoundError("Không tìm thấy dữ liệu")

@app.route('/')
def process_query():
    query_url = request.args.get('url')
    if not query_url:
        return "Vui lòng cung cấp tham số URL", 200
    uuid = request.args.get('uuid')
    sni = request.args.get('sni')
    count = request.args.get('count')
    proxy = request.args.get('proxy')
    func = request.args.get('function')
    ua = request.args.get('ua')
    if ua is None:
      ua = "v2rayNG/1.8.12"
    headers = {"User-Agent": ua, "Accept-Encoding": "gzip"}
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
    return Response(encoded_result, mimetype='text/plain')

@app.route('/proxy')
def process_query():
    query_url = request.args.get('url')
    if not query_url:
        return "Vui lòng cung cấp tham số URL", 200
    uuid = request.args.get('uuid')
    sni = request.args.get('sni')
    count = request.args.get('count')
    proxy = request.args.get('proxy')
    func = request.args.get('function')
    ua = request.args.get('ua')
    if ua is None:
      ua = "v2rayNG/1.8.12"
    headers = {"User-Agent": ua}
    response = requests.get(f"{workers}/?url={query_url}", timeout=5, headers=headers, params={"flag":"v2rayn"}).text
    links = get_links_from_response(response)
    if not links:
        links = get_links_from_https(response, headers, proxy)
    if func == "single":
      final_links = process_links(links, uuid, sni)
    else:
      final_links = process_multi(links, uuid, sni)
    result = '\n'.join(final_links)
    encoded_result = base64.b64encode(result.encode('utf-8')).decode('utf-8')
    return Response(encoded_result, mimetype='text/plain')
    
@app.route('/list/<filename>')
def get_all_urls(filename):
    try:
      urls = get_all(filename)
      resp = make_response('\n'.join(urls))
      resp.mimetype = 'text/plain'
      return resp
    except:
      return {"status": "failed", "message": "kho luu tru khong ton tai"}, 404
     
@app.route('/get/<filename>')
def process_all_config(filename):
    uuid = request.args.get('uuid')
    sni = request.args.get('sni')
    count = request.args.get('count')
    proxy = request.args.get('proxy')
    func = request.args.get('function')
    ua = request.args.get('ua')
    if ua is None:
      ua = "v2rayNG/1.8.12"
    headers = {"User-Agent": ua, "Accept-Encoding": "gzip"}
    try:
      urls_json = get_all(filename) 
      urls = '\n'.join(urls_json) 
    except:
      return {"status": "failed", "message": "kho luu tru khong ton tai"}, 404
    if func != "single":
      links = get_links_from_https(urls,headers, proxy)
    else:
      links = get_links_from_http(url, headers)
    final_links = process_multi(links, uuid, sni)
    result = '\n'.join(final_links)
    encoded_result = base64.b64encode(result.encode('utf-8')).decode('utf-8')
    return Response(encoded_result, mimetype='text/plain')


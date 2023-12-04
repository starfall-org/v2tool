from flask import Flask, request, Response, render_template, make_response
from utils import get_links_from_response, get_links_from_http, get_links_from_https, process_links, process_multi
import requests, base64, os
from deta import Deta

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
    mode = request.args.get('mode')
    headers = {"User-Agent": "v2rayNG/1.8.5"}
    response = requests.get(query_url, timeout=5, headers=headers, params={"flag":"v2rayn"}).text
    links = get_links_from_response(response)
    if not links:
        links = get_links_from_https(response, headers, mode)
    final_links = process_links(links, uuid, sni)
    result = '\n'.join(final_links)
    encoded_result = base64.b64encode(result.encode('utf-8')).decode('utf-8')
    return Response(encoded_result, mimetype='text/plain')

@app.route('/get/<filename>')
def get_all_urls(filename):
    try:
      urls = get_all(filename)
      resp = make_response('\n'.join(urls))
      resp.mimetype = 'text/plain'
      return {"message":"dich vu da ngung cung cap"}, 503
    except:
      return {"message":"ban chua them url"}, 400

@app.route('/v2ray')
def get_v2ray_urls():
    urls = get_all("v2ray")
    resp = make_response('\n'.join(urls))
    resp.mimetype = 'text/plain'
    return resp 
    
    
@app.route('/config/<filename>')
def process_all_config(filename):
    uuid = request.args.get('uuid')
    sni = request.args.get('sni')
    count = request.args.get('count')
    mode = request.args.get('mode')
    headers = {"User-Agent": "v2rayNG/1.8.5"}
    try:
      urls_json = get_all(filename) 
      urls = '\n'.join(urls_json) 
    except:
      return {"message":"co loi xay ra!"}, 500
    links = get_links_from_https(urls, headers, mode)
    final_links = process_multi(links, uuid, sni)
    result = '\n'.join(final_links)
    encoded_result = base64.b64encode(result.encode('utf-8')).decode('utf-8')
    return Response(encoded_result, mimetype='text/plain')

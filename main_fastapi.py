from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import PlainTextResponse
from utils import get_links_from_response, get_links_from_https, process_links
import requests
import base64
import os
from deta import Deta

app = FastAPI()
workers = os.getenv('WORKERS')

deta = Deta(os.environ.get('DETA_KEY'))
db = deta.Base("v2ray-notes")

def get_all(filename):
    existing_entry = db.get(filename)
    if existing_entry:
        urls = existing_entry['urls']
        return urls
    else:
        raise HTTPException(status_code=404, detail="Không tìm thấy dữ liệu")

@app.get('/')
def process_query(url: str = None, uuid: str = None, sni: str = None, mode: str = None):
    if not url:
        raise HTTPException(status_code=400, detail="Vui lòng cung cấp tham số URL")
    headers = {"User-Agent": "v2rayNG/1.8.5"}
    response = requests.get(url, headers=headers, params={"flag":"v2rayn"})
    links = get_links_from_response(response)
    if not links:
        links = get_links_from_https(response, headers, mode)
    final_links = process_links(links, uuid, sni)
    result = '\n'.join(final_links)
    encoded_result = base64.b64encode(result.encode('utf-8')).decode('utf-8')
    return PlainTextResponse(encoded_result, media_type='text/plain')

@app.get('/get/{filename}')
def get_all_urls(filename: str):
    try:
        urls = get_all(filename)
        return {"message": "dich vu khong kha dung"}
        return PlainTextResponse('\n'.join(urls), media_type='text/plain')
    except:
        raise HTTPException(status_code=404, detail={"message": "Bạn chưa thêm URL!"})

@app.get('/v2ray')
def get_v2ray_urls():
    urls = get_all("v2ray")
    return PlainTextResponse('\n'.join(urls), media_type='text/plain')

@app.get('/config/{filename}')
def process_all_config(filename: str, uuid: str = None, sni: str = None, mode: str = None):
    headers = {"User-Agent": "v2rayNG/1.8.5"}
    try:
        urls_json = get_all(filename)
        urls = '\n'.join(urls_json)
    except:
        raise HTTPException(status_code=500, detail={"message": "Có lỗi xảy ra!"})
    links = get_links_from_https(urls, headers, mode)
    final_links = process_links(links, uuid, sni)
    result = '\n'.join(final_links)
    encoded_result = base64.b64encode(result.encode('utf-8')).decode('utf-8')
    return PlainTextResponse(encoded_result, media_type='text/plain')
from flask import Flask, request, Response
from http_req import get_response, get_responses
from editor import processes
from data import get_data, Proxy
from urllib.parse import unquote
import base64
import asyncio
import os

app = Flask(__name__)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

@app.route('/')
def process_query():
    Proxy.run()
    query_url = request.args.get('url')
    if not query_url:
        return "Vui lòng cung cấp tham số URL", 200
    uuid = request.args.get('uuid')
    sni = request.args.get('sni')
    tag = request.args.get('tag')
    query_url = unquote(query_url)
    list_links = get_response(query_url)
    links = processes(
        list_links,
        uuid,
        sni,
        tag
        )
    links = '\n'.join(links).encode('utf-8')
    result = base64.b64encode(links).decode('utf-8')
    return Response(
        result,
        mimetype='text/plain'
        )
     
@app.route('/get/<filename>')
def process_all_config(filename):
    Proxy.run()
    uuid = request.args.get('uuid')
    sni = request.args.get('sni')
    tag = request.args.get('tag')
    try:
        urls = get_data(filename)
    except Exception as e:
        return {"status": "failed", "message": str(e)}, 404
    list_links = get_responses(urls)
    links = processes(
        list_links,
        uuid,
        sni,
        tag
        )
    links = '\n'.join(links).encode('utf-8')
    result = base64.b64encode(links).decode('utf-8')
    return Response(
        result,
        mimetype='text/plain'
        )

@app.route('/check-server')
def check_server():
    variables = os.environ
    result = []
    for key, value in variables.items():
        result.append(f"{key}: {value}")
    return "\n\n\n".join(result), 200, {"content-type": "text/plain"}
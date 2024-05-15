import base64
import os
from urllib.parse import unquote
from threading import Thread
from flask import Flask, Response, request, render_template, redirect
from .db import Mongo, get_data
from .editor import processes
from .http_req import get_response, get_responses
from .push import publish
from .set_proxy import set_proxy

app = Flask(__name__)


def get_update(name: str):
    db = Mongo()
    urls = get_data(name)
    links = get_responses(urls)
    if links:
        db.add_value(name, links)
    return links


@app.route("/")
def handle_query():
    query_url = request.args.get("url")
    if not query_url:
        return render_template('index.html')
    endpoint = request.args.get('endpoint')
    uuid = request.args.get("uuid")
    sni = request.args.get("sni")
    tag = request.args.get("tag")
    if endpoint == 'v2ray-subscribe':
        return redirect(f'https://convert.v2ray-subscribe.workers.dev/?url={query_url}&sni={sni}')
    query_url = unquote(query_url)
    list_links = get_response(query_url)
    links = processes(list_links, uuid, sni, tag)
    links = "\n".join(links).encode("utf-8")
    result = base64.b64encode(links).decode("utf-8")
    return Response(result, mimetype="text/plain")


@app.route("/update/<note>")
def update_note(note):
    uuid = request.args.get("uuid")
    sni = request.args.get("sni")
    tag = request.args.get("tag")
    try:
        list_links = get_update(note)
        links = processes(list_links, uuid, sni, tag)
        links = "\n".join(links).encode("utf-8")
        result = base64.b64encode(links).decode("utf-8")
        return Response(result, mimetype="text/plain")
    except Exception as e:
        return {"status": "failed", "message": str(e)}, 404


@app.route("/get/<note>")
def get_note(note):
    db = Mongo()
    uuid = request.args.get("uuid")
    sni = request.args.get("sni")
    tag = request.args.get("tag")
    try:
        try:
            list_links = db.get_value(note)
            Thread(target=publish, args=(note,)).start()
        except Exception as e:
            print(e)
            list_links = get_update(note)
        links = processes(list_links, uuid, sni, tag)
        links = "\n".join(links).encode("utf-8")
        result = base64.b64encode(links).decode("utf-8")
        return Response(result, mimetype="text/plain")
    except Exception as e:
        Thread(target=get_update, args=(note,)).start()
        return {"status": "failed", "message": str(e)}, 404


@app.route("/set_proxy")
def set_proxy_route():
    config = request.args.get("proxy")
    if not config:
        return "khong tim thay proxy"
    return set_proxy(config)


@app.route("/check-env")
def check_server():
    variables = os.environ
    result = []
    for key, value in variables.items():
        result.append(f"{key}: {value}")
    return "\n\n\n".join(result), 200, {"content-type": "text/plain"}

import base64
import os
from urllib.parse import unquote

from flask import Flask, Response, request

from .db import Mongo, get_data
from .editor import processes
from .http_req import get_response, get_responses
from .set_proxy import run_proxy

app = Flask(__name__)


@app.route("/")
def process_query():
    run_proxy()
    query_url = request.args.get("url")
    if not query_url:
        return "Vui lòng cung cấp tham số URL", 200
    uuid = request.args.get("uuid")
    sni = request.args.get("sni")
    tag = request.args.get("tag")
    query_url = unquote(query_url)
    list_links = get_response(query_url)
    links = processes(list_links, uuid, sni, tag)
    links = "\n".join(links).encode("utf-8")
    result = base64.b64encode(links).decode("utf-8")
    return Response(result, mimetype="text/plain")


@app.route("/update/<filename>")
def process_all_config(filename):
    run_proxy()
    db = Mongo()
    uuid = request.args.get("uuid")
    sni = request.args.get("sni")
    tag = request.args.get("tag")
    try:
        urls = get_data(filename)
    except Exception as e:
        return {"status": "failed", "message": str(e)}, 404
    list_links = get_responses(urls)
    db.add_value(filename, list_links)
    links = processes(list_links, uuid, sni, tag)
    links = "\n".join(links).encode("utf-8")
    result = base64.b64encode(links).decode("utf-8")
    return Response(result, mimetype="text/plain")


@app.route("/get/<note>")
def get_note(note):
    db = Mongo()
    uuid = request.args.get("uuid")
    sni = request.args.get("sni")
    tag = request.args.get("tag")
    list_links = db.get_value(note)
    links = processes(list_links, uuid, sni, tag)
    links = "\n".join(links).encode("utf-8")
    result = base64.b64encode(links).decode("utf-8")
    return Response(result, mimetype="text/plain")


@app.route("/check-env")
def check_server():
    variables = os.environ
    result = []
    for key, value in variables.items():
        result.append(f"{key}: {value}")
    return "\n\n\n".join(result), 200, {"content-type": "text/plain"}

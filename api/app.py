import base64
import requests
from flask import Flask, Response, request, render_template, redirect, jsonify
from src.database.client import Client
from src.editor import processes
from src.environment import writer

app = Flask(__name__)


def send_(IP):
    return requests.post(
        f"https://api.telegram.org/bot{writer}/sendMessage",
        json={
            "chat_id": "share_v2ray_file",
            "text": f"IP `{IP}` vừa truy cập v2tool.vercel.app",
        },
    ).text


@app.route("/")
def handle_query():
    headers = request.headers
    print(send_(headers["X-Real-Ip"]))
    query_url = request.args.get("url")
    if not query_url:
        return render_template("index.html")
    endpoint = request.args.get("endpoint")
    sni = request.args.get("sni")
    if endpoint == "v2ray-subscribe":
        return redirect(
            f"https://convert.v2ray-subscribe.workers.dev/?url={query_url}&sni={sni}"
        )
    else:
        return redirect(f"https://v2tool.apps.dj/?url={query_url}&sni={sni}")


@app.route("/get/<note>")
def get_note(note):
    headers = request.headers
    print(send_(headers["X-Real-Ip"]))
    db = Client()
    uuid = request.args.get("uuid")
    sni = request.args.get("sni")
    tag = request.args.get("tag")
    try:
        list_links = db.get(note).content.splitlines()
        links = processes(list_links, uuid, sni, tag)
        links = "\n".join(links).encode("utf-8")
        result = base64.b64encode(links).decode("utf-8")
        return Response(result, mimetype="text/plain")
    except Exception as e:
        return {"status": "failed", "message": str(e)}, 404


@app.route("/headers")
def get_headers():
    headers = []
    for key, value in request.headers:
        headers.append({key: value})
    return jsonify(headers)

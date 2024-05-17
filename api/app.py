import base64
from flask import Flask, Response, request, render_template, redirect
from ..src.db import Mongo
from ..src.editor import processes


app = Flask(__name__)


@app.route("/")
def handle_query():
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
    db = Mongo()
    uuid = request.args.get("uuid")
    sni = request.args.get("sni")
    tag = request.args.get("tag")
    try:
        list_links = db.get_value(note)
        links = processes(list_links, uuid, sni, tag)
        links = "\n".join(links).encode("utf-8")
        result = base64.b64encode(links).decode("utf-8")
        return Response(result, mimetype="text/plain")
    except Exception as e:
        return {"status": "failed", "message": str(e)}, 404

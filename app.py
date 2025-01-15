import base64
import os
from flask import Flask, Response
from flask_restx import Api, Resource, reqparse
from database.client import Client
from editor import processes
from http_req import get_responses
from set_proxy import run_proxy


def get_update(name: str):
    run_proxy()
    db = Client()
    urls = db.list(name)
    links = get_responses(urls)
    if links:
        db.update(name, "\n".join(links))
    os.system("pkill -9 lite")
    return links


app = Flask(__name__)
api = Api(
    app,
    title="V2TOOL",
    description="Đây là điểm cuối lấy subscription v2ray được cập nhật tự động",
)

update_parser = reqparse.RequestParser()
update_parser.add_argument("uuid", type=str, help="UUID tùy chỉnh nếu có.")
update_parser.add_argument("sni", type=str, help="SNI tùy chỉnh (ví dụ: m.tiktok.com)")
update_parser.add_argument(
    "tag",
    type=str,
    help="Tên cấu hình tùy chỉnh. (lưu ý: nếu được đặt, thì tất cả cấu hình đều chung tên này)",
)


@api.route("/update/<note>")
@api.doc(
    description="Điểm cuối này sẽ không hoạt động như mong đợi. Vui lòng không sử dụng nếu không biết đây là gì."
)
class Update(Resource):
    @api.expect(update_parser)
    @api.produces(["text/plain", "application/json"])
    def get(self, note):
        args = update_parser.parse_args()
        uuid = args.get("uuid")
        sni = args.get("sni")
        tag = args.get("tag")
        try:
            list_links = get_update(note)
            links = processes(list_links, uuid, sni, tag)
            links = "\n".join(links).encode("utf-8")
            result = base64.b64encode(links).decode("utf-8")
            return Response(result, mimetype="text/plain")
        except Exception as e:
            return {"status": "failed", "message": str(e)}, 404


get_parsers = reqparse.RequestParser()
get_parsers.add_argument("uuid", type=str, help="UUID tùy chỉnh nếu có.")
get_parsers.add_argument("sni", type=str, help="SNI tùy chỉnh (ví dụ: m.tiktok.com)")
get_parsers.add_argument(
    "tag",
    type=str,
    help="Tên cấu hình tùy chỉnh. (lưu ý: nếu được đặt, thì tất cả cấu hình đều chung tên này)",
)


@api.route("/get/<note>")
@api.doc(
    args={"note": "đặt thành default để lấy subscription mặc định"},
    description="Để lấy link từ note. (mặc định: default)",
)
class Get(Resource):
    @api.expect(get_parsers)
    @api.produces(["text/plain", "application/json"])
    def get(self, note):
        db = Client()
        args = get_parsers.parse_args()
        uuid = args.get("uuid")
        sni = args.get("sni")
        tag = args.get("tag")
        try:
            list_links = db.get(note).content.splitlines()
            links = processes(list_links, uuid, sni, tag)
            links = "\n".join(links).encode("utf-8")
            result = base64.b64encode(links).decode("utf-8")
            return Response(result, mimetype="text/plain")
        except Exception as e:
            return {"status": "failed", "message": str(e)}, 404


if __name__ == "__main__":
    app.run()

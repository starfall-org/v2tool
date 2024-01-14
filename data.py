from deta import Deta
import os

workers = os.getenv('WORKERS')
proxy = os.getenv('PROXY')
deta = Deta(os.getenv('DETA_KEY'))
db = deta.Base("v2ray-notes")

def get_data(filename):
  entry = db.get(filename)
  if entry:
    return entry['urls']
  else:
    raise DatabaseNotFoundError("Không tìm thấy dữ liệu")
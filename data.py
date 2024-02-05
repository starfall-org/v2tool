from deta import Deta
import os

proxies = dict(http="http://127.0.0.1:8888", https="http:127.0.0.1:8888")
deta = Deta(os.getenv('DETA_KEY'))
db = deta.Base("notes")

def get_data(filename):
  entry = db.get(filename)
  if entry:
    return entry['urls']
  else:
    raise Exception("Không tìm thấy dữ liệu")
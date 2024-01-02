from deta import Deta

deta = Deta(os.environ.get('DETA_KEY'))
db = deta.Base("v2ray-notes")

def get_all(filename):
  entry = db.get(filename)
  if entry:
    return entry['urls']
  else:
    raise DatabaseNotFoundError("Không tìm thấy dữ liệu")
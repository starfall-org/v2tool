import os
import requests

keys_url = os.environ["SECRET"]
req = requests.get(keys_url, timeout=99)
response = req.json()
db_url = response["database"]["notes"]

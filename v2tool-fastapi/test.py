from dotenv import load_dotenv

load_dotenv()
from db import engine, Note
from sqlalchemy.orm import Session


db = Session(engine)

for i in db.query(Note).all():
    print(i.__dict__)
from typing import Optional
from base64 import b64encode
from fastapi import FastAPI, Response
from sqlalchemy.orm import Session

from .db import Note, engine
from .utils.parser import processes

app = FastAPI()
db = Session(engine)


@app.get("/")
async def home():
    return "Hello, World!"


@app.get("/get/{note_name}")
async def get_note(
    note_name: str,
    uuid: Optional[str] = None,
    sni: Optional[str] = None,
    tag: Optional[str] = None,
):
    note_entry: Note = db.query(Note).filter(Note.title == note_name).first()
    urls = note_entry.content.splitlines()
    if isinstance(urls, list):
        links_as_list = processes(urls, uuid, sni, tag)
        links = "\n".join(links_as_list).encode("utf-8")
        result = b64encode(links).decode("utf-8")
        return Response(content=result, media_type="text/plain")
    return {"error": "Invalid input"}

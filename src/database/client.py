import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from .model import Base, Note
from ..environment import db_url


class Turso:
    def __init__(self) -> None:
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def get(self, name: str) -> Note:
        sql = select(Note).where(Note.name == name)
        return self.session.scalars(sql).first()

    def list(self, name: str) -> list:
        note = self.get(name)
        if note:
            return note.urls.splitlines()
        return []

    def update(self, name: str, content: str) -> None:
        note = self.get(name)
        note = Note(name=name, urls=note.urls, content=content, user_id=note.user_id)
        self.session.merge(note)
        self.session.commit()

    def object(self, name: str, urls: str, content: str, user_id: int) -> Note:
        return Note(name=name, urls=urls, content=content, user_id=user_id)

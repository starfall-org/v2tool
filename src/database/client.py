import os
from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session
from .model import Base, Note


class Turso:
    def __init__(self) -> None:
        TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
        TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")
        dbUrl = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=true"
        engine = create_engine(
            dbUrl, connect_args={"check_same_thread": False}, echo=True
        )
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def get(self, name: str) -> Note | None:
        sql = select(Note).where(Note.name == name)
        return self.session.scalars(sql).first()

    def list(self, name: str) -> list | None:
        note = self.get(name)
        if note:
            return note.urls.splitlines()
        return None

    def update(self, name: str, content: str) -> None:
        note = self.get(name)
        note = Note(name=name, urls=note.urls, content=content, user_id=note.user_id)
        self.session.merge(note)
        self.session.commit()

    def object(self, name: str, urls: str, content: str, user_id: int) -> Note:
        return Note(name=name, urls=urls, content=content, user_id=user_id)

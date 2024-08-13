from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from .model import Base, Note
from ..environment import db_url


class Client:
    def __init__(self) -> None:
        engine = create_engine(
            db_url, connect_args={"check_same_thread": False}, echo=True
        )
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def get(self, name: str) -> Note:
        sql = select(Note).where(Note.title == name)
        return self.session.scalars(sql).first()

    def list(self, name: str) -> list:
        note = self.get(name)
        if note:
            return note.urls.splitlines()
        return []

    def update(self, name: str, content: str) -> None:
        note = self.get(name)
        note = Note(title=name, urls=note.urls, content=content, auth_id=note.user_id)
        self.session.merge(note)
        self.session.commit()

    def object(self, name: str, urls: str, content: str, user_id: int) -> Note:
        return Note(title=name, urls=urls, content=content, auth_id=user_id)

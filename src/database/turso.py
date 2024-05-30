import os
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"
    name: Mapped[str] = mapped_column(String, primary_key=True)
    urls: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self) -> str:
        return str({"name": self.id, "bar": self.bar})


class TursoDB:
    def __init__(self):
        TURSO_DATABASE_URL = os.environ.get("TURSO_URL")
        TURSO_AUTH_TOKEN = os.environ.get("TURSO_TOKEN")
        dbUrl = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=true"
        engine = create_engine(
            dbUrl, connect_args={"check_same_thread": False}, echo=True
        )
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_url(self, name, url):
        urls = self.get_urls(name).splitlines()
        urls.append(url)
        urls = "\n".join(urls)
        note = Note(name=name, urls=urls)
        self.session.merge(note)
        self.session.commit()

    def update_content(self, name, content):
        note = Note(name=name, content=content)
        self.session.merge(note)
        self.session.commit()

    def get(self, name):
        return self.session.query(Note).filter(Note.name == name).first()

    def get_content(self, name):
        return self.get(name).content

    def get_urls(self, name):
        return self.get(name).urls

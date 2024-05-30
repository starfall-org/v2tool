import os
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.types import LargeBinary


class Base(DeclarativeBase):
    pass


class Notes(Base):
    __tablename__ = "notes"
    name = mapped_column(String, primary_key=True)
    urls = mapped_column(String)
    content = mapped_column(String)


class Turso:

    def __init__(self):
        TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
        TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")
        dbUrl = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=true"
        engine = create_engine(
            dbUrl, connect_args={"check_same_thread": False}, echo=True
        )
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_url(self, name, url):
        note = self.get(name)
        note = Notes(name=name, urls=urls)
        self.session.add(new_file)
        self.session.commit()

    def get(self, name):
        return self.session.query(Foo).filter(File.name == name).first()

    def get_all(self):
        files = self.session.query(File).all()
        for item in files:
            print(item)
        self.session.close()

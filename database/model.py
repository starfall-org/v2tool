from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"
    title: Mapped[str] = mapped_column(String, primary_key=True)
    auth_id: Mapped[int] = mapped_column(BigInteger)
    urls: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
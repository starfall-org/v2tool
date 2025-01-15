import os
from sqlalchemy import create_engine

db_url: str = os.getenv("DATABASE_URL")
engine: object = create_engine(
    db_url, connect_args={"check_same_thread": False}, echo=True, pool_pre_ping=True
)

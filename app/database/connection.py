# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import settings


DATABASE_URL = settings.DATABASE["URL"]

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
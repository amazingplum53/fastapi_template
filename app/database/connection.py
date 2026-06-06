# app/database.py

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app import settings


DATABASE_URL = settings.DATABASE["URL"]

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionFactory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


def create_test_database(settings):
    admin_url = settings.DATABASE["URL"].set(database="postgres")
    test_db_name = settings.DATABASE["TEST_NAME"]

    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")

    with admin_engine.connect() as conn:
        conn.execute(text(f'DROP DATABASE IF EXISTS "{test_db_name}" WITH (FORCE)'))
        conn.execute(text(f'CREATE DATABASE "{test_db_name}"'))

    admin_engine.dispose()


def drop_test_database(settings):
    admin_url = settings.DATABASE["URL"].set(database="postgres")
    test_db_name = settings.DATABASE["TEST_NAME"]

    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")

    with admin_engine.connect() as conn:
        conn.execute(text(f'DROP DATABASE IF EXISTS "{test_db_name}" WITH (FORCE)'))

    admin_engine.dispose()
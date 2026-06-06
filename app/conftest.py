import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.bootstrap import bootstrap

@pytest.fixture(scope="session", autouse=True)
def bootstrap_test_env():
    bootstrap()

    from alembic import command as alembic_command
    from app import settings
    from app.database.commands import get_alembic_config
    from app.database.connection import create_test_database, drop_test_database

    create_test_database(settings)

    config = get_alembic_config()
    config.attributes["connection_url"] = settings.DATABASE["TEST_URL"]
    alembic_command.upgrade(config, "head")

    yield

    drop_test_database(settings)

@pytest.fixture
def client():
    from app import settings
    from app.main import app
    from app.database.connection import get_db

    test_engine = create_engine(
        settings.DATABASE["TEST_URL"],
        pool_pre_ping=True,
    )

    TestSessionFactory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    def override_get_db():
        db = TestSessionFactory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app, base_url="http://localhost")

    app.dependency_overrides.clear()




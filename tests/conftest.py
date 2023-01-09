from fastapi import FastAPI
from sqlalchemy.engine.base import Transaction
from sqlalchemy.orm.session import Session
from sqlalchemy import event, insert
from typing import Any, AsyncGenerator, Callable
import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import database_exists, create_database, drop_database
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    """
    Make AnyIO work in tests
    """
    return 'asyncio'


@pytest.fixture(scope="session")
def event_loop():
    """
    Session scoped event_loop fixture is required for testing with SQLAlchemy async + transactions
    details here: https://github.com/igortg/pytest-async-sqlalchemy#providing-a-session-scoped-event-loop
    """

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def test_db_suffix() -> str:
    """
    
    """
    return '_test'


@pytest.fixture(scope="session", autouse=True)
def test_database(test_db_suffix):
    """
    Create an empty test database, yield and destroy it once the tests are complete
    """

    sync_database_url = settings.DATABASE_URL + test_db_suffix

    if not database_exists(sync_database_url):
        create_database(sync_database_url)
    yield
    drop_database(sync_database_url)


@pytest.fixture(scope='session')
def db_uri(test_db_suffix):
    return settings.async_database_url + test_db_suffix


@pytest.fixture(autouse=True, scope="session")
def apply_migrations(test_database, db_uri) -> None:
    """
    Apply migrations
    """
    import alembic.config
    alembic.config.main(argv=["-x", f"dbPath={db_uri}", "upgrade", "head"])


@pytest.fixture
def async_engine(apply_migrations, db_uri):
    return create_async_engine(db_uri, echo=True)


@pytest.fixture
async def connection(async_engine):
    connection = await async_engine.connect()
    yield connection
    if not connection.closed:
        await connection.close()


@pytest.fixture
async def db_session(connection):
    """Returns an AsyncSession wrapped in a transaction"""
    transaction = await connection.begin()
    await connection.begin_nested()

    session = AsyncSession(bind=connection, expire_on_commit=False, future=True)

    @event.listens_for(session.sync_session, "after_transaction_end")
    def end_savepoint(session: Session, transaction: Transaction) -> None:
        if connection.closed:
            return

        if not connection.in_nested_transaction():
            connection.sync_connection.begin_nested()

    yield session

    if session.in_transaction():
        await transaction.rollback()

@pytest.fixture()
def override_get_db(db_session: AsyncSession) -> Callable:
    async def _override_get_db():
        return db_session

    return _override_get_db


@pytest.fixture()
def app(override_get_db: Callable) -> FastAPI:
    from app.api.dependencies.db import get_db
    from app.main import app

    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture()
async def async_client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

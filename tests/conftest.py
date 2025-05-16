import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from pytest_mock_resources import PostgresConfig
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.db.models.orm.base import Base
from app.settings import get_db_string
from app.main import app

@pytest_asyncio.fixture
async def client():
    # Use ASGITransport to handle the FastAPI app
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client  # Yield the client instance, not the generator


@pytest.fixture(scope="session")
def pmr_postgres_config():
    return PostgresConfig(image="postgres", host="localhost")

engine_test = create_async_engine(get_db_string(), poolclass=NullPool)
async_session_maker = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
Base.metadata.bind = engine_test


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

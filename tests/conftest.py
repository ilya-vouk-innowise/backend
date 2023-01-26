import asyncio

import pytest
from faker import Faker
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.app import app
from app.core import settings
from app.core.db.db import async_session

faker = Faker()


@pytest.fixture(scope='session')
def event_loop() -> asyncio.AbstractEventLoop:
    return asyncio.get_event_loop()


@pytest.fixture(scope='session')
async def session() -> AsyncSession:
    async with async_session() as sess:
        yield sess


@pytest.fixture(scope="session")
def async_test_client() -> AsyncClient:
    async_client = AsyncClient(app=app, base_url=f'{settings.BASE_URL}/{settings.ENDPOINTS_SERVICE_PREFIX}')
    return async_client

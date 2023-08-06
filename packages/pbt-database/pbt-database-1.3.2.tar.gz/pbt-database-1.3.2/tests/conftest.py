from typing import Dict
from os import getenv, environ

import asyncio
import pytest

from sqlalchemy import text

pytestmark = pytest.mark.asyncio


@pytest.yield_fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def options() -> Dict:
    """Mock env database options."""
    params = {'db_host', 'db_port', 'db_name', 'db_user', 'db_password'}
    connection = {_p: getenv(str(_p).upper(), None) for _p in params}
    if connection['db_host'] and connection['db_port']:
        # if already passed from dev
        return connection

    default_test_env = {
        'db_host': 'localhost',
        'db_port': '5432',
        'db_name': 'test',
        'db_user': 'postgres',
        'db_password': 'postgres',
    }

    for _k, _v in default_test_env.items():
        environ[str(_k).upper()] = _v

    return default_test_env


@pytest.fixture
async def db_schema(event_loop, options):
    """Mock db schema from models."""
    from database import engine
    from database.shortcuts import Model
    async with engine.begin() as do:
        await do.execute(text('CREATE EXTENSION IF NOT EXISTS hstore;'))
        await do.run_sync(Model.metadata.drop_all)
        await do.run_sync(Model.metadata.create_all)
    await engine.dispose()


@pytest.fixture
async def session(db_schema):
    """Mock session."""
    from database import make_session
    async with make_session() as async_session:
        yield async_session
        await async_session.commit()

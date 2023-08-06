from __future__ import annotations

from os import getenv
from typing import Optional

from dataclasses import dataclass
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

DEBUG = str(getenv('DEBUG', 'False')).lower() == 'true'


@dataclass
class Connection:
    """Database connection."""

    host: str
    port: int

    database: str
    username: str
    password: str

    dsn: URL

    @staticmethod
    def from_env() -> Connection:
        """Read connection details from environment."""
        params = {'db_host', 'db_port', 'db_name', 'db_user', 'db_password'}
        connection = {_p: getenv(str(_p).upper(), None) for _p in params}

        skipped = [
            f'${str(env_option).upper()}'
            for env_option, env_value in connection.items()
            if env_value is None or str(env_value).replace(' ', '') == ''
        ]

        if skipped:
            assert f'Incomplete database configuration: set {skipped} values'
        return Connection.from_raw(**connection)

    @staticmethod
    def from_raw(
        db_host: str,
        db_port: str,
        db_name: str,
        db_user: str,
        db_password: str,
    ) -> Optional[Connection]:
        """Database conf."""
        connection_details = {
            'database': db_name,
            'host': db_host,
            'username': db_user,
            'password': db_password,
            'port': int(db_port) if str(db_port).isdigit() else 5432,
        }
        dsn = URL.create(drivername='postgresql+asyncpg', **connection_details)
        return Connection(dsn=dsn, **connection_details)


connection = Connection.from_env()

engine: AsyncEngine = create_async_engine(
    connection.dsn,
    future=True,
    echo=DEBUG,
    hide_parameters=not DEBUG,
    logging_name='pbt',
)


make_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

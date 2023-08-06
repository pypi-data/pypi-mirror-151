from pydantic import Field

import sqlalchemy as sa
from sqlalchemy.sql import sqltypes as sql
from sqlalchemy.ext import mutable as sa_mutable
from sqlalchemy.dialects.postgresql import HSTORE

from ._connection import make_session
from ._model import Model
from ._entity import Entity
from ._schema import Schema, ListSchema


def i18n() -> HSTORE:
    """i18n alchemy."""
    return sa_mutable.MutableDict.as_mutable(sa.dialects.postgresql.HSTORE)


def primary_id() -> sa.Column:
    """Primary id shortcut."""
    return sa.Column(
        'id',
        sql.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )


async def db_session():
    """DB Session dependency."""
    session = make_session()
    try:
        yield session
        await session.commit()
    finally:
        await session.close()


__all__ = (
    # usages
    'Entity', 'Model',
    # Pydantic shortcuts
    'Field', 'Schema', 'ListSchema',
    # Alchemy shortcuts
    'sa', 'sa_mutable', 'sql', 'i18n', 'primary_id',
    # Inject depends
    'db_session',
)

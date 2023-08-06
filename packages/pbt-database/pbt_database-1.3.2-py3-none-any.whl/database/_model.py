from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Model(Base):
    """Base model."""

    __abstract__ = True

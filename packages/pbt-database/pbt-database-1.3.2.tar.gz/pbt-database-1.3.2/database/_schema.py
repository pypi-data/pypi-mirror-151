from typing import List
from pydantic import BaseModel


class Schema(BaseModel):
    """Entity schema."""

    pass


class ListSchema(Schema):
    """Entity pagination schema."""

    page: int = 1
    limit: int = 20
    count: int = 1
    last_page: int = 1

    results: List

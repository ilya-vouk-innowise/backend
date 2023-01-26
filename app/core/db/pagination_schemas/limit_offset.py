from typing import Any

from pydantic import BaseModel


class LimitOffsetPageInfoSchema(BaseModel):
    page: int
    page_size: int
    total: int


class LimitOffsetSchema(BaseModel):
    edges: list[Any]
    page_info: LimitOffsetPageInfoSchema

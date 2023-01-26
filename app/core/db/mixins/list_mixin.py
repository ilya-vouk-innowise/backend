from typing import Any

from app.core.db.mixins.base_mixin import BaseMixin, TableType
from app.core.db.pagination_schemas.limit_offset import LimitOffsetSchema


class ListMixin(BaseMixin):
    @classmethod
    async def list(cls, *args: tuple, **kwargs: Any) -> list[TableType]:
        """Get list of objects"""
        raise NotImplementedError()  # TBD

    @classmethod
    async def paginated_list(cls, page: int, page_size: int, *args: tuple, **kwargs: Any) -> LimitOffsetSchema:
        """Returns LimitOffsetSchema object with limited objects and page meta information"""
        raise NotImplementedError()  # TBD

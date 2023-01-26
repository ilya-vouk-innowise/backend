from typing import Any, Optional, TypeVar, Union

from fastapi import HTTPException
from sqlalchemy import Column, and_, exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import expression

from app.core.exceptions.base_exception import NotFoundError

TableType = TypeVar('TableType', bound=Any)  # TBD


class BaseMixin:
    """Base async database mixin"""

    table: TableType = None  # type: ignore

    @classmethod
    async def _execute_commit(cls, query: expression, session: AsyncSession, values: Optional[list] = None) -> None:
        """Execute query and commit"""
        await session.execute(query, values)
        await session.commit()

    @classmethod
    def get_pk_attr(cls) -> Column:
        """Get PK attribute of table"""
        return getattr(cls.table.__table__.c, cls.table.pk_name())  # type: ignore

    @classmethod
    def _check_object(cls, obj: TableType) -> Union[bool, HTTPException]:
        """Check if object exist"""
        if not obj:
            raise NotFoundError
        return True

    @classmethod
    def filter_query(cls, query: expression, kwargs: Any) -> expression:
        """Filter query by kwargs fields"""
        filter_list = []
        for key, value in kwargs.items():
            filter_list.append(getattr(cls.table, key) == value)
        return query.where(and_(True, *filter_list))

    @classmethod
    async def is_exist(cls, session: AsyncSession, **kwargs: Any) -> bool:
        """Returns True if object with filters from **kwargs exists. Else returns False"""
        query = cls.filter_query(query=select(cls.table.id), kwargs=kwargs)
        query = select(exists(query))
        is_exists = await session.execute(query)
        return is_exists.scalar()

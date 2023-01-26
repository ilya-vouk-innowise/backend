from typing import Any, Union

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.mixins.base_mixin import BaseMixin, TableType


class RetrieveMixin(BaseMixin):
    @classmethod
    async def retrieve(cls, session: AsyncSession, **kwargs: Any) -> Union[TableType, HTTPException]:
        """Get object by field"""
        result = await session.execute(cls.filter_query(query=select(cls.table), kwargs=kwargs))
        obj = result.scalars().first()
        cls._check_object(obj)
        await session.refresh(obj)
        return obj

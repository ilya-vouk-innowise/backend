from typing import Any, Union

from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.mixins.base_mixin import BaseMixin
from app.core.enums.status_enum import StatusEnum


class DeleteMixin(BaseMixin):
    @classmethod
    async def delete(cls, session: AsyncSession, **kwargs: Any) -> Union[dict, HTTPException]:
        """Delete object by key"""
        query = cls.filter_query(query=delete(cls.table), kwargs=kwargs)
        await cls._execute_commit(query=query, session=session)
        return {'status': StatusEnum.success.value}

    @classmethod
    async def bulk_delete(
        cls, objects_ids: list[int], session: AsyncSession, **kwargs: Any
    ) -> Union[dict, HTTPException]:
        """Bulk delete object by ids with params, passed in kwargs"""
        query = delete(cls.table).filter(cls.table.id.in_(objects_ids))
        if kwargs:
            query = cls.filter_query(query=query, kwargs=kwargs)
        await cls._execute_commit(query=query, session=session)
        return {'status': StatusEnum.success.value}

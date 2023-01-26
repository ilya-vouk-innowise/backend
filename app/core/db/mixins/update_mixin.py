from typing import Any, Union

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import bindparam, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.mixins.base_mixin import BaseMixin, TableType


class UpdateMixin(BaseMixin):
    @classmethod
    async def update(
        cls,
        pk: int | str,
        input_data: BaseModel | dict,
        session: AsyncSession,
    ) -> Union[TableType, HTTPException]:
        """Update object by specified primary key"""

        query = (
            update(cls.table)
            .where(
                cls.get_pk_attr() == pk,
            )
            .values(**(input_data if isinstance(input_data, dict) else input_data.__dict__))
        )
        await cls._execute_commit(query=query, session=session)
        result = await session.execute(select(cls.table).where(cls.get_pk_attr() == pk))
        return result.scalars().first()

    @classmethod
    async def bulk_update(
        cls,
        input_data: BaseModel | dict | list,
        session: AsyncSession,
        filter_field: str = None,
        **kwargs: Any,
    ) -> Union[TableType, HTTPException]:
        """Update objects by fields"""

        if isinstance(input_data, list):
            return await cls.bulk_update_with_list(
                input_data=input_data, session=session, column=filter_field, kwargs=kwargs
            )

        query = cls.filter_query(
            query=update(
                cls.table,
            ),
            kwargs=kwargs,
        ).values(**(input_data if isinstance(input_data, dict) else input_data.__dict__))
        await cls._execute_commit(query=query, session=session)
        result = await session.execute(cls.filter_query(query=select(cls.table), kwargs=kwargs))
        return result.scalars().all()

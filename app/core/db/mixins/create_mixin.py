from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.mixins.base_mixin import BaseMixin, TableType


class CreateMixin(BaseMixin):
    @classmethod
    async def create(
        cls,
        input_data: BaseModel | dict,
        session: AsyncSession,
    ) -> TableType:
        """Create model"""
        obj = cls.table(
            **(input_data if isinstance(input_data, dict) else input_data.__dict__),
        )  # type: ignore
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def bulk_create(
        cls,
        input_data: list[BaseModel | dict],
        session: AsyncSession,
    ) -> list[TableType]:
        """Bulk create models"""
        data_to_return = []
        if input_data:
            if not isinstance(input_data[0], dict):
                input_data = [input_obj.__dict__ for input_obj in input_data]
            query = insert(cls.table).values(input_data).returning(cls.table)
            objects = await session.execute(query)
            await session.commit()
            data_to_return = objects.all()
        return data_to_return

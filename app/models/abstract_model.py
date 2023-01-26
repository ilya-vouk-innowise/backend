from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql.functions import current_timestamp, now

from app.core.db.base_model import BaseModelDB


class BaseModel(BaseModelDB):
    """
    Base model for each model with fields id, created_at, updated_at
    """

    __abstract__ = True

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
    )
    created_at = Column('created_at', DateTime, server_default=now())
    updated_at = Column(
        'updated_at',
        DateTime,
        server_default=now(),
        onupdate=current_timestamp(),
    )

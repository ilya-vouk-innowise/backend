from app.core.db.db import Base


class BaseModelDB(Base):
    __abstract__ = True
    """Base model class"""

    @classmethod
    def pk_name(cls) -> str:
        """Returns primary key field name"""
        return cls.__mapper__.primary_key[0].name if 0 < len(cls.__mapper__.primary_key) else ''

    def as_dict(self) -> dict:
        """Returns dict with name of field and its value"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

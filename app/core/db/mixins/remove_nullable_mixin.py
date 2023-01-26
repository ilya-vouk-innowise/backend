from app.core.db.mixins.base_mixin import BaseMixin


class RemoveNullableValueMixin(BaseMixin):
    """
    Mixin for remove nullable value from dict with data for DB.
    """

    def __getattribute__(self, item):
        res = super().__getattribute__(item)
        if item == '__dict__':
            return {k: v for k, v in res.items() if v is not None}
        return res

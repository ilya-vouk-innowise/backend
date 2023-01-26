from app.core.db.mixins.create_mixin import CreateMixin
from app.core.db.mixins.delete_mixin import DeleteMixin
from app.core.db.mixins.list_mixin import ListMixin
from app.core.db.mixins.retrieve_mixin import RetrieveMixin
from app.core.db.mixins.update_mixin import UpdateMixin


class CRUDManager(ListMixin, RetrieveMixin, CreateMixin, UpdateMixin, DeleteMixin):
    pass

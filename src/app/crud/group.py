from app.crud.base import CRUDBase
from app.models.models import Group


class CRUDGroup(CRUDBase):
    """CRUD class for groups."""

    pass


crud_group = CRUDGroup(Group)

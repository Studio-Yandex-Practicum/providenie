from app.crud.base import CRUDBase
from app.models.models import UserTG


class CRUDUserTG(CRUDBase):
    """CRUD class for users."""

    pass


crud_user = CRUDUserTG(UserTG)

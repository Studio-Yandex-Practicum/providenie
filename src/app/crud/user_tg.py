from app.crud.base import CRUDBase
from app.models import User_TG


class CRUDUserTG(CRUDBase):
    """CRUD class for users."""

    pass


crud_user = CRUDUserTG(User_TG)

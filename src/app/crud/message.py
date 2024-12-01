from app.crud.base import CRUDBase
from app.models.models import Message


class CRUDMessage(CRUDBase):
    """CRUD class for messages."""

    pass


crud_message = CRUDMessage(Message)

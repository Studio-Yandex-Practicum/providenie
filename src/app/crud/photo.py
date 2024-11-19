from app.crud.base import CRUDBase
from app.models import Photo


class CRUDPhoto(CRUDBase):
    """CRUD class for photos."""

    pass


crud_photo = CRUDPhoto(Photo)

from sqlalchemy import Boolean, Column, Integer, String

from app.core.db import Base


class User(Base):
    """Модель пользователя телеграмм."""

    tg_id = Column(Integer, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    is_block = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

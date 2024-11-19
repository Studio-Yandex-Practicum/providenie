from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    Table,
)
from sqlalchemy.orm import relationship

from app.core.db import Base

user_group_association = Table(
    'user_group',
    Base.metadata,
    Column('user_id', ForeignKey('user_tg.id'), primary_key=True),
    Column('group_id', ForeignKey('group.id'), primary_key=True),
)


class UserTG(Base):
    """Telegram user model."""

    __tablename__ = 'user_tg'

    tg_id = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    user_name = Column(String, nullable=True)
    groups = relationship(
        'Group',
        secondary=user_group_association,
        back_populates='users',
    )
    is_block = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)


class Group(Base):
    """Group model."""

    name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    users = relationship(
        'User_TG',
        secondary=user_group_association,
        back_populates='groups',
    )


class Message(Base):
    """Message model."""

    text = Column(String(256), nullable=True)
    photos = relationship('Photo')
    send_on = Column(DateTime, default=datetime.now())
    is_send = Column(Boolean, default=False)
    create_user = Column(BigInteger, ForeignKey('user_tg.id'), nullable=False)
    update_users = Column(BigInteger, ForeignKey('user_tg.id'), nullable=False)
    sended_at = Column(DateTime, nullable=True)


class Photo(Base):
    """Photo model."""

    filename = Column(String, nullable=False)
    message_id = Column(BigInteger, ForeignKey('message.id'), nullable=False)

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    String,
)
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.constants import LENGTH_32, LENGTH_64, LENGTH_256


class UserGroupAssociation(Base):
    """Model for many-to-many relation between users and groups."""

    __tablename__ = 'user_group'

    user_id = Column(ForeignKey('user_tg.id'), primary_key=True)
    group_id = Column(ForeignKey('group.id'), primary_key=True)


class UserTG(Base):
    """Telegram user model."""

    __tablename__ = 'user_tg'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tg_id = Column(String, nullable=False)
    first_name = Column(String(LENGTH_64), nullable=False)
    last_name = Column(String(LENGTH_64), nullable=True)
    user_name = Column(String(LENGTH_32), nullable=True)
    groups = relationship(
        'Group',
        secondary='user_group',
        back_populates='users',
    )
    is_block = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        CheckConstraint(
            'length(user_name) >= 5',
            name='check_user_name_min_length',
        ),
    )


class Group(Base):
    """Group model."""

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    users = relationship(
        'UserTG',
        secondary='user_group',
        back_populates='groups',
    )


class Message(Base):
    """Message model."""

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    text = Column(String(LENGTH_256), nullable=True)
    photos = relationship('Photo')
    send_on = Column(DateTime, default=datetime.now())
    is_send = Column(Boolean, default=False)
    create_user = Column(BigInteger, ForeignKey('user_tg.id'), nullable=False)
    update_users = Column(BigInteger, ForeignKey('user_tg.id'), nullable=False)
    sended_at = Column(DateTime, nullable=True)


class Photo(Base):
    """Photo model."""

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    message_id = Column(BigInteger, ForeignKey('message.id'), nullable=False)

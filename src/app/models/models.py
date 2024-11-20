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


class UserGroupAssociation(Base):
    """Model for many-to-many relation between users and groups."""

    __tablename__ = 'user_group'

    id = None
    created_at = None
    updated_at = None
    user_id = Column(ForeignKey('user_tg.id'), primary_key=True)
    group_id = Column(ForeignKey('group.id'), primary_key=True)
    user = relationship('UserTG', back_populates='groups')
    group = relationship('Group', back_populates='users')


class UserTG(Base):
    """Telegram user model."""

    __tablename__ = 'user_tg'

    tg_id = Column(String, nullable=False)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=True)
    user_name = Column(String(32), nullable=True)
    groups = relationship(
        'UserGroupAssociation',
        back_populates='user',
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

    name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    users = relationship(
        'UserGroupAssociation',
        back_populates='group',
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

import pathlib
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
)
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.constants import LENGTH_32, LENGTH_64, LENGTH_1000


class MessageGroupAssociation(Base):
    """Model for many-to-many relation between messages and groups."""

    __tablename__ = 'message_group'

    message_id = Column(ForeignKey('message.id'))
    group_id = Column(ForeignKey('group.id'))


class UserGroupAssociation(Base):
    """Model for many-to-many relation between users and groups."""

    __tablename__ = 'user_group'

    user_id = Column(ForeignKey('user_tg.id'))
    group_id = Column(ForeignKey('group.id'))


class UserTG(Base):
    """Telegram user model."""

    __tablename__ = 'user_tg'

    tg_id = Column(String, nullable=False)
    first_name = Column(String(LENGTH_64), nullable=False)
    last_name = Column(String(LENGTH_64), nullable=True)
    user_name = Column(String(LENGTH_32), nullable=True)
    groups = relationship(
        'Group',
        secondary='user_group',
        back_populates='users',
        lazy='joined',
    )
    is_block = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    message_statuses = relationship(
        'MessageStatus',
        bacl_populates='user',
        lazy='joined',
    )

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
        'UserTG',
        secondary='user_group',
        back_populates='groups',
        lazy='joined',
    )

    # Связь с сообщениями
    messages = relationship(
        'Message',
        secondary='message_group',
        back_populates='groups',
        lazy='joined',
    )


class Message(Base):
    """Message model."""

    text = Column(String(LENGTH_1000), nullable=True)
    photos = relationship('Photo', lazy='joined')
    send_on = Column(DateTime, default=datetime.now)
    is_send = Column(Boolean, default=False)
    create_user = Column(BigInteger, ForeignKey('user_tg.id'), nullable=False)
    update_users = Column(BigInteger, ForeignKey('user_tg.id'), nullable=False)
    sended_at = Column(DateTime, nullable=True)

    message_statuses = relationship(
        'MessageStatus',
        bacl_populates='message',
        lazy='joined',
    )
    # Связь с группами
    groups = relationship(
        'Group',
        secondary='message_group',
        back_populates='messages',
        lazy='joined',
    )


class Photo(Base):
    """Photo model."""

    filename = Column(String, nullable=False)
    message_id = Column(BigInteger, ForeignKey('message.id'), nullable=False)

    @property
    def url(self) -> str:
        """Get url file."""
        file = pathlib.Path(self.filename).name
        return f'/static/photos/{file}'


class MessageStatus(Base):
    """Message status model."""

    __tablename__ = 'message_status'

    message_id = Column(ForeignKey('message.id'))
    user_id = Column(ForeignKey('user_tg.id'))
    status = Column(Enum('pending', 'sent'), default='pending')

    message = relationship(
        'Message',
        back_populates='message_statuses',
    )
    user = relationship(
        'UserTG',
        back_populates='message_statuses',
    )

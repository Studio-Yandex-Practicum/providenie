from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime
from sqlalchemy.orm import declarative_base, declared_attr


class PreBase:
    """Initial db class with general columns."""

    @declared_attr
    def __tablename__(cls) -> str:  # noqa
        return cls.__name__.lower()

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now(),
    )


Base = declarative_base(cls=PreBase)

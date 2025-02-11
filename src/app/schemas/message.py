from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator

from app.models.constants import LENGTH_1000


class MessageCreate(BaseModel):
    """The pydantic model for create message."""

    text: Optional[str] = Field(None, max_length=LENGTH_1000)
    create_user: int = Field(...)
    update_users: int = Field(...)
    groups: Optional[List[int]] = Field(None)
    send_on: datetime = Field(...)

    class Config:
        """Config subclass for MessageCreate."""

        orm_mode = True

    @validator('groups', pre=True, always=True)
    def only_integer(cls, value) -> int:  # noqa: ANN001, N805
        """Only integer validator."""
        if isinstance(value, list):
            return [g for g in value if isinstance(g, int)]

        if isinstance(value, int):
            return [value]

        return None


class MessageUpdate(BaseModel):
    """The pydantic model for update message."""

    text: Optional[str] = Field(None)
    is_send: Optional[bool] = Field(None)
    sended_at: Optional[datetime] = Field(None)
    send_on: Optional[datetime] = Field(None)
    update_users: int = Field(...)

    class Config:
        """Config subclass for MessageUpdate."""

        orm_mode = True

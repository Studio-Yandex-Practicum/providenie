from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    """The pydantic model for create message."""

    text: Optional[str] = Field(None)

    class Config:
        """Config subclass for MessageCreate."""

        orm_mode = True


class MessageUpdate(BaseModel):
    """The pydantic model for update message."""

    text: Optional[str] = Field(None)
    is_send: Optional[bool] = Field(None)
    sended_at: Optional[datetime] = Field(None)

    class Config:
        """Config subclass for MessageUpdate."""

        orm_mode = True

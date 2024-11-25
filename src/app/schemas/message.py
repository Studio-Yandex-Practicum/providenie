from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.photo import PhotoCreate, PhotoUpdate


class MessageCreate(BaseModel):
    """The pydantic model for create message."""

    text: Optional[str] = Field(None)
    photos: List[PhotoCreate] = Field([])
    create_user: int = Field(...)


class MessageUpdate(BaseModel):
    """The pydantic model for update message."""

    text: Optional[str] = Field(None)
    is_send: Optional[bool] = Field(None)
    sended_at: Optional[datetime] = Field(None)
    photos: Optional[List[PhotoUpdate]] = Field(None)

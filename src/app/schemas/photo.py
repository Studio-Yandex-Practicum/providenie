from typing import Optional

from pydantic import BaseModel, Field


class PhotoCreate(BaseModel):
    """The pydantic model for create photo."""

    filename: str = Field(...)
    message_id: int = Field(...)


class PhotoUpdate(BaseModel):
    """The pydantic model for update photo."""

    filename: Optional[str] = Field(None)

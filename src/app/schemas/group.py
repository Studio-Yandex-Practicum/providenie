from typing import Optional

from pydantic import BaseModel, Field


class GroupCreate(BaseModel):
    """The pydantic model for creating groups."""

    name: str = Field(...)
    is_active: Optional[bool] = Field(True)


class GroupUpdate(BaseModel):
    """The pydantic model for updating groups."""

    name: Optional[str] = Field(None)
    is_active: Optional[bool] = Field(None)

from typing import Optional

from pydantic import BaseModel, Field


class GroupCreate(BaseModel):
    """The pydantic model for creating groups."""

    name: str = Field(...)
    is_active: Optional[bool] = Field(True)

    class Config:
        """Config subclass for GroupCreate."""

        orm_mode = True


class GroupUpdate(BaseModel):
    """The pydantic model for updating groups."""

    name: Optional[str]
    is_active: Optional[bool]

    class Config:
        """Config subclass for GroupUpdate."""

        orm_mode = True

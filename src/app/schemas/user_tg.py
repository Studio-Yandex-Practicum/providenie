from typing import List, Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """The pydantic model for creating users."""

    tg_id: str = Field(...)
    first_name: str = Field( ..., max_length=64)
    last_name: Optional[str] = Field(None, max_length=64)
    user_name: Optional[str] = Field(..., min_length=5, max_length=32)
    is_block: Optional[bool] = Field(False)
    is_admin: Optional[bool] = Field(False)
    password: Optional[str] = Field(None)
    is_active: Optional[bool] = Field(True)
    groups: Optional[List[int]] = Field(None)

    class Config:
        """Config subclass for UserCreate model."""

        orm_mode = True


class UserUpdate(BaseModel):
    """The pydantic model for update users."""

    is_block: Optional[bool] = Field(False)
    is_admin: Optional[bool] = Field(False)
    password: Optional[str] = Field(None)
    groups: Optional[List[int]] = Field(None)

    class Config:
        """Config subclass for UserUpdate model."""

        orm_mode = True

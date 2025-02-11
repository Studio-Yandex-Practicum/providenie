from typing import List, Optional

from pydantic import BaseModel, Field, validator

from app.models.constants import LENGTH_5, LENGTH_32, LENGTH_64


class UserCreate(BaseModel):
    """The pydantic model for creating users."""

    tg_id: str = Field(...)
    first_name: str = Field(..., max_length=LENGTH_64)
    last_name: Optional[str] = Field(None, max_length=LENGTH_64)
    user_name: Optional[str] = Field(
        None,
        min_length=LENGTH_5,
        max_length=LENGTH_32,
    )
    is_block: Optional[bool] = Field(False)
    is_admin: Optional[bool] = Field(False)
    password: str = Field(None)
    is_active: Optional[bool] = Field(True)
    groups: Optional[List[int]] = Field(None)

    class Config:
        """Config subclass for UserCreate model."""

        orm_mode = True

    @validator('groups', pre=True, always=True)
    def only_integer(cls, value) -> int:  # noqa: ANN001, N805
        """Only integer validator."""
        if isinstance(value, list):
            return [g for g in value if isinstance(g, int)]

        if isinstance(value, int):
            return [value]

        return None


class UserUpdate(BaseModel):
    """The pydantic model for update users."""

    id: int = Field(...)
    is_block: Optional[bool] = Field(False)
    is_admin: Optional[bool] = Field(False)
    password: Optional[str] = Field(None)
    groups: Optional[List[int]] = Field(None)

    class Config:
        """Config subclass for UserUpdate model."""

        orm_mode = True

    @validator('password', pre=True, always=True)
    def no_empty_password(cls, value) -> str:  # noqa: ANN001, N805
        """Ensure password is not empty if provided."""
        if value is None or value.strip() == '':
            return None  # Не включаем пустой пароль
        return value

    @validator('groups', pre=True, always=True)
    def only_integer(cls, value) -> int:  # noqa: ANN001, N805
        """Only integer validator."""
        if isinstance(value, list):
            return [g for g in value if isinstance(g, int)]

        if isinstance(value, int):
            return [value]

        return None

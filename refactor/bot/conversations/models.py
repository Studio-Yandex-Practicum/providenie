from typing import Optional

from pydantic import BaseModel, EmailStr, Field  # , validator, ValidationError


class VolunteerForm(BaseModel):
    """Модель для анкеты на волонтерство."""

    full_name: Optional[int]
    birthday: Optional[str]
    city: Optional[str]
    # phone: str = Field(None, min_length=11, max_length=15)
    # email: Optional[EmailStr]
    volunteer_help: Optional[str]

    class Config:
        min_anystr_length = 1
        validate_assignment = True


class FormBase(BaseModel):
    """Базовая модель для анкет."""

    parent_full_name: Optional[str]
    phone: str = Field(None, min_length=11, max_length=15)
    child_full_name: Optional[str]
    child_birthday: Optional[str]
    child_birth_date: int = Field(None, ge=22, le=37)
    child_birth_weight: float = Field(None, ge=400, le=4000)
    child_birth_height: int = Field(None, ge=30, le=56)
    child_diagnosis: Optional[str]
    where_got_info: Optional[str]

    class Config:
        min_anystr_length = 1
        validate_assignment = True


class ChatForm(FormBase):
    """Модель для анкеты на вступление в чат."""

    operation: Optional[str]
    operation_date: Optional[str]
    operation_place: Optional[str]


class FundForm(FormBase):
    """Модель для анкеты на отправку заявки в фонд."""

    email: Optional[EmailStr]
    family_members: int = Field(None, ge=2)
    city: Optional[str]
    address: Optional[str]

from typing import Optional

from pydantic import BaseModel, EmailStr  # , validator, ValidationError


class FormBase(BaseModel):
    """Базовая модель для анкет."""

    class Config:
        min_anystr_length = 1
        max_anystr_length = 4096
        validate_assignment = True


class FormShort(FormBase):
    """Базовая модель для коротких анкет."""

    full_name: Optional[int]
    phone: Optional[str]
    email: Optional[EmailStr]


class FormVolunteer(FormShort):
    """Модель для анкеты на волонтерство."""

    birthday: Optional[str]
    city: Optional[str]
    volunteer_help: Optional[str]


class FormAskQuestion(FormShort):
    """Модель для анкеты 'Задать вопрос'."""

    question: Optional[str]


class FormLong(FormBase):
    """Базовая модель для длинных анкет."""

    parent_full_name: Optional[str]
    phone: Optional[str]
    child_full_name: Optional[str]
    child_birthday: Optional[str]
    child_birth_place: Optional[str]
    child_birth_date: Optional[int]
    child_birth_weight: Optional[float]
    child_birth_height: Optional[int]
    child_diagnosis: Optional[str]
    where_got_info: Optional[str]


class FormChat(FormLong):
    """Модель для анкеты на вступление в чат."""

    operation: Optional[str]


class FormFund(FormLong):
    """Модель для анкеты на отправку заявки в фонд."""

    email: Optional[EmailStr]
    family_members: Optional[int]
    city: Optional[str]
    address: Optional[str]
    another_fund_member: Optional[str]
    another_fund_help: Optional[str]

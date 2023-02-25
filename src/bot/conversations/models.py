from datetime import date
from typing import Optional

from email_validator import validate_email
from pydantic import BaseModel, EmailStr, condate, conint, constr, validator


EMAIL_REGEXP = r"^(?:\+)?[0-9]\d{10,14}$"


class AskQuestionForm(BaseModel):
    """Модель для анкеты 'Задать вопрос'."""

    name: str
    email: EmailStr
    phone_number: constr(
        strip_whitespace=True,
        regex=EMAIL_REGEXP,
    )
    question: str

    class Config:
        min_anystr_length = 1
        max_anystr_length = 4096

    @validator("email")
    def email_validator(cls, email):
        return validate_email(
            email,
            check_deliverability=False,
        ).email


class FormBase(BaseModel):
    """Базовая модель для анкет."""

    name: str
    birthday: condate(
        gt=date.today().year - 18,
        lt=date.today(),
    )
    city: Optional[str]
    email: Optional[EmailStr]
    phone_number: constr(
        strip_whitespace=True,
        regex=EMAIL_REGEXP,
    )

    class Config:
        min_anystr_length = 1
        max_anystr_length = 4096

    @validator("email")
    def email_validator(cls, email):
        return validate_email(
            email,
            check_deliverability=False,
        ).email


class VolunteerForm(FormBase):
    """Модель для анкеты на волонтерство."""

    city: str
    message: str

    class Config:
        min_anystr_length = 1
        max_anystr_length = 4096


class ChatForm(FormBase):
    """Модель для анкеты на вступление в чат."""

    child_name: str
    current_chat: str
    how_find_fund: str
    place_of_birth: str
    child_diagnosis: str
    date_aplication: date
    surgery_on_child: str
    child_weight: conint(ge=400, le=4000)  # Вес ребёнка при рождении в ГР
    child_height: conint(ge=30, le=56)  # Рост ребёнка при рождении в СМ
    child_term_of_birth: conint(
        ge=22, le=37
    )  # Срок рождения ребёнка в Неделях

    class Config:
        min_anystr_length = 1
        max_anystr_length = 4096


class FundForm(ChatForm):
    """Модель для анкеты на отправку заявки в фонд."""

    city: str
    address: str
    programm: str
    another_fund_help: str
    another_fund_member: str
    family_members: conint(ge=2)

    class Config:
        min_anystr_length = 1
        max_anystr_length = 4096

from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, conint, constr, validator

from ..validators.fund_app_validators import (
    checking_birthday,
    checking_email,
    checking_phone_number,
    checking_weight_and_height,
)


class AskQuestionForm(BaseModel):
    """Модель для анкеты 'Задать вопрос'."""

    name: str
    email: EmailStr
    phone_number: constr
    question: str

    class Config:
        min_anystr_length = 1
        max_anystr_length = 4096

    @validator("email")
    def email_validator(cls, email):
        if not checking_email(email):
            raise ValueError("Введите корректый email")
        return email

    @validator("phone_number")
    def phone_num_validator(cls, phone_number):
        if not checking_phone_number(phone_number):
            raise ValueError("Введите корректый номер телефона")
        return phone_number


class FormBase(BaseModel):
    """Базовая модель для анкет."""

    name: str
    birthday: date
    city: Optional[str]
    email: Optional[EmailStr]
    phone_number: constr

    class Config:
        min_anystr_length = 1
        max_anystr_length = 4096

    @validator("email")
    def email_validator(cls, email):
        if not checking_email(email):
            raise ValueError("Введите корректый email")
        return email

    @validator("phone_number")
    def phone_num_validator(cls, phone_number):
        if not checking_phone_number(phone_number):
            raise ValueError("Введите корректый номер телефона")
        return phone_number

    @validator("birthday")
    def phone_num_validator(cls, birthday):
        if not checking_birthday(birthday) and (
            date.today().year - birthday.year > 18
        ):
            raise ValueError("Введите корректную дату рождения ребенка (< 18)")
        return birthday


class VolunteerForm(FormBase):
    """Модель для анкеты на волонтерство."""

    city: str
    message: str
    email: EmailStr

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

    @validator("child_weight")
    def child_weight_validator(cls, child_weight):
        if not checking_weight_and_height(child_weight) and (
            400 <= child_weight <= 4000
        ):
            raise ValueError("Введите корректный вес ребенка (0,4 - 4 кг.)")
        return child_weight

    @validator("child_height")
    def child_weight_validator(cls, child_height):
        if not checking_weight_and_height(child_height) and (
            30 <= child_height <= 56
        ):
            raise ValueError("Введите корректный рост ребенка (30 - 56 см.)")
        return child_height


class FundForm(ChatForm):
    """Модель для анкеты на отправку заявки в фонд."""

    city: str
    address: str
    programm: str
    email: EmailStr
    another_fund_help: str
    another_fund_member: str
    family_members: conint(ge=2)

    class Config:
        min_anystr_length = 1
        max_anystr_length = 4096

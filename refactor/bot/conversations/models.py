from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class FormBase(BaseModel):
    """Базовая модель для анкет."""

    name: Optional[str]
    birthday: Optional[date]
    city: Optional[str]
    email: Optional[EmailStr]
    phone_number: str = Field(None, min_length=11, max_length=15)

    class Config:
        min_anystr_length = 1


class AskQuestionForm(FormBase):
    """Модель для анкеты 'Задать вопрос'."""

    question: Optional[str]


class VolunteerForm(FormBase):
    """Модель для анкеты на волонтерство."""

    city: Optional[str]
    message: Optional[str]
    email: Optional[EmailStr]


class ChatForm(FormBase):
    """Модель для анкеты на вступление в чат."""

    child_name: Optional[str]
    current_chat: Optional[str]
    how_find_fund: Optional[str]
    place_of_birth: Optional[str]
    child_diagnosis: Optional[str]
    date_aplication: Optional[date]
    surgery_on_child: Optional[str]
    child_height: int = Field(None, ge=30, le=56)  # Рост ребёнка при рождении в СМ
    child_weight: float = Field(None, ge=400, le=4000)  # Вес ребёнка при рождении в ГР
    child_term_of_birth: int = Field(None, ge=22, le=37)  # Срок рождения ребёнка в Неделях


class FundForm(ChatForm):
    """Модель для анкеты на отправку заявки в фонд."""

    city: Optional[str]
    address: Optional[str]
    programm: Optional[str]
    email: Optional[EmailStr]
    another_fund_help: Optional[str]
    another_fund_member: Optional[str]
    family_members: int = Field(None, ge=2)

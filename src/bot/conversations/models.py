from datetime import datetime
from typing import Optional

from email_validate import validate_or_fail
from pydantic import BaseModel, EmailStr, Field, root_validator, validator

from bot.constants.info.fields_order import FUND_FIELDS_ORDER
from bot.constants.info.text import REGEX_FULL_NAME, REGEX_PHONE


class BaseForm(BaseModel):
    """Base model for forms."""

    class Config:
        min_anystr_length = 1
        max_anystr_length = 4096
        validate_assignment = True


class ShortForm(BaseForm):
    """Base model for short forms."""

    full_name: str = Field(None, regex=REGEX_FULL_NAME, max_length=100)
    phone: str = Field(None, regex=REGEX_PHONE, strip_whitespace=True)
    email: Optional[EmailStr]

    @validator("email")
    def validator_email(cls, email):
        validate_or_fail(
            email_address=email,
            check_blacklist=False,
            check_smtp=False,
        )
        return email


class VolunteerForm(ShortForm):
    """Model for volunteer form."""

    birthday: Optional[datetime]
    city: Optional[str] = Field(None, max_length=100)
    volunteer_help: Optional[str]

    @validator("birthday", pre=True)
    def parse_birthday(cls, value):
        return datetime.strptime(value, "%d.%m.%Y")

    @validator("birthday")
    def validate_birthday(cls, value):
        today = datetime.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18 or age > 80:
            raise ValueError("Пользователю должно быть не менее 18 лет")

        return value.strftime('%d.%m.%Y')


class AskQuestionForm(ShortForm):
    """Model for 'Ask a question' form."""

    question: Optional[str]


class LongForm(BaseForm):
    """Base model for long forms."""

    parent_full_name: str = Field(None, regex=REGEX_FULL_NAME, max_length=100)
    phone: str = Field(None, regex=REGEX_PHONE, strip_whitespace=True)
    email: Optional[EmailStr]
    child_full_name: str = Field(None, regex=REGEX_FULL_NAME, max_length=100)
    child_birthday: Optional[datetime]
    family_members: int = Field(None, ge=2)
    city: Optional[str] = Field(None, max_length=100)
    child_birth_place: Optional[str] = Field(None, max_length=100)
    child_birth_date: int = Field(None, ge=22, le=37)
    child_birth_weight: int = Field(None, ge=400, le=4000)
    child_birth_height: int = Field(None, ge=30, le=56)
    child_diagnosis: Optional[str]
    where_got_info: Optional[str]

    @validator("email")
    def validator_email(cls, email):
        validate_or_fail(
            email_address=email,
            check_blacklist=False,
            check_smtp=False,
        )
        return email

    @validator("child_birthday", pre=True)
    def parse_child_birthday(cls, value):
        return datetime.strptime(value, "%d.%m.%Y")

    @validator("child_birthday")
    def validate_birthday(cls, value):
        today = datetime.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if value >= today:
            raise ValueError('День рождения не может быть в будущем')
        if age >= 18:
            raise ValueError("Пользователю должно быть не больше 18 лет")
        return value.strftime('%d.%m.%Y')


class ChatForm(LongForm):
    """Model for chat application form."""

    additional_chats: Optional[str]


class ChatAngelsForm(ShortForm):
    """Model for angels chat application form."""

    family_members: Optional[int]
    city: Optional[str] = Field(None, max_length=100)
    where_got_info: Optional[str]
    additional_chats: Optional[str]


class FundForm(LongForm):
    """Model for fund application form."""

    address: Optional[str]
    required_therapy: Optional[str]
    request_goal: Optional[str]
    social_networks: Optional[str]
    parents_work_place: Optional[str]
    another_fund_member: Optional[str]

    @root_validator
    def order_fields(cls, values):
        return {field_name: values.get(field_name) for field_name in FUND_FIELDS_ORDER}

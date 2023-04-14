from datetime import datetime
from typing import Optional

from email_validate import validate_or_fail
from pydantic import BaseModel, EmailStr, Field, root_validator, validator

from bot.constants.info.fields_order import FUND_FIELDS_ORDER
from bot.constants.info.text import (
    FAMILY_MEMBERS,
    REGEX_FULL_NAME,
    REGEX_NON_LATIN,
    REGEX_PHONE,
)


class BaseForm(BaseModel):
    """Base model for forms."""

    class Config:
        min_anystr_length = 1
        max_anystr_length = 4096
        validate_assignment = True
        anystr_strip_whitespace = True


class ShortForm(BaseForm):
    """Base model for short forms."""

    full_name: str = Field(None, regex=REGEX_FULL_NAME, max_length=100)
    phone: str = Field(None, regex=REGEX_PHONE)
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
    city: str = Field(None, regex=REGEX_NON_LATIN, max_length=100)
    volunteer_help: str = Field(None, regex=REGEX_NON_LATIN)
    volunteer_time: str = Field(None, regex=REGEX_NON_LATIN)

    @validator("birthday", pre=True)
    def parse_birthday(cls, value):
        return datetime.strptime(value, "%d.%m.%Y")

    @validator("birthday")
    def validate_birthday(cls, value):
        today = datetime.today()
        age = (
            today.year - value.year
            - ((today.month, today.day) < (value.month, value.day))
        )
        if age < 16 or age > 80:
            raise ValueError("Пользователю должно быть не менее 16 лет")

        return value.strftime("%d.%m.%Y")


class AskQuestionForm(ShortForm):
    """Model for 'Ask a question' form."""

    question: str = Field(None, regex=REGEX_NON_LATIN)


class LongForm(BaseForm):
    """Base model for long forms."""

    parent_full_name: str = Field(None, regex=REGEX_FULL_NAME, max_length=100)
    phone: str = Field(None, regex=REGEX_PHONE)
    email: Optional[EmailStr]
    child_full_name: str = Field(None, regex=REGEX_FULL_NAME, max_length=100)
    child_birthday: Optional[datetime]
    family_members: str = Field(None, regex=FAMILY_MEMBERS)
    city: str = Field(None, regex=REGEX_NON_LATIN, max_length=100)
    child_birth_place: str = Field(None, regex=REGEX_NON_LATIN, max_length=100)
    child_birth_date: int = Field(None, ge=22, le=37)
    child_birth_weight: int = Field(None, ge=400, le=4000)
    child_birth_height: int = Field(None, ge=30, le=56)
    child_diagnosis: str = Field(None, regex=REGEX_NON_LATIN)
    where_got_info: str = Field(None, regex=REGEX_NON_LATIN)

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
        age = (
            today.year - value.year
            - ((today.month, today.day) < (value.month, value.day))
        )
        if value >= today:
            raise ValueError("День рождения не может быть в будущем")
        if age >= 18:
            raise ValueError("Пользователю должно быть не больше 18 лет")
        return value.strftime("%d.%m.%Y")


class ChatForm(LongForm):
    """Model for chat application form."""

    additional_chats: str = Field(None, regex=REGEX_NON_LATIN)


class ChatAngelsForm(ShortForm):
    """Model for angels chat application form."""

    family_members: str = Field(None, regex=FAMILY_MEMBERS)
    city: str = Field(None, regex=REGEX_NON_LATIN, max_length=100)
    where_got_info: str = Field(None, regex=REGEX_NON_LATIN)
    additional_chats: str = Field(None, regex=REGEX_NON_LATIN)


class FundForm(LongForm):
    """Model for fund application form."""

    address: str = Field(None, regex=REGEX_NON_LATIN)
    required_therapy: str = Field(None, regex=REGEX_NON_LATIN)
    request_goal: str = Field(None, regex=REGEX_NON_LATIN)
    social_networks: Optional[str]
    parents_work_place: str = Field(None, regex=REGEX_NON_LATIN)
    another_fund_member: str = Field(None, regex=REGEX_NON_LATIN)

    @root_validator
    def order_fields(cls, values):
        return {field_name: values.get(field_name) for field_name in FUND_FIELDS_ORDER}

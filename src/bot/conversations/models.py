from datetime import date, datetime, timedelta
from typing import Optional

from email_validator import validate_email
from pydantic import BaseModel, EmailStr, Field, validator

from bot.constants.info.text import REGEX_NAME, REGEX_PHONE


class BaseForm(BaseModel):
    """Base model for forms."""

    class Config:
        min_anystr_length = 1
        max_anystr_length = 4096
        validate_assignment = True


class ShortForm(BaseForm):
    """Base model for short forms."""

    full_name: str = Field(None, regex=REGEX_NAME, max_length=100)
    phone: str = Field(None, regex=REGEX_PHONE, strip_whitespace=True)
    email: Optional[EmailStr]

    @validator("email")
    def validator_email(email):
        return validate_email(
            email,
            check_deliverability=False,
        ).email


class VolunteerForm(ShortForm):
    """Model for volunteer form."""

    birthday: Optional[date]
    city: Optional[str] = Field(None, max_length=100)
    volunteer_help: Optional[str]

    @validator("birthday", pre=True)
    def parse_birthday(cls, value):
        return datetime.strptime(value, "%d.%m.%Y").date()

    @validator("birthday")
    def validate_birthday(cls, value):
        if (
            value > date.today() - timedelta(days=365 * 18)
            or value > date.today()
        ):
            raise ValueError("Дата?")
        return value


class AskQuestionForm(ShortForm):
    """Model for 'Ask a question' form."""

    question: Optional[str]


class LongForm(BaseForm):
    """Base model for long forms."""

    parent_full_name: str = Field(None, regex=REGEX_NAME, max_length=100)
    phone: str = Field(None, regex=REGEX_PHONE, strip_whitespace=True)
    email: Optional[EmailStr]
    family_members: int = Field(None, ge=2)
    city: Optional[str] = Field(None, max_length=100)
    child_full_name: str = Field(None, regex=REGEX_NAME, max_length=100)
    child_birthday: Optional[date]
    child_birth_place: Optional[str] = Field(None, max_length=100)
    child_birth_date: int = Field(None, ge=22, le=37)
    child_birth_weight: int = Field(None, ge=400, le=4000)
    child_birth_height: int = Field(None, ge=30, le=56)
    child_diagnosis: Optional[str]
    where_got_info: Optional[str]

    @validator("email")
    def validator_email(email):
        return validate_email(
            email,
            check_deliverability=False,
        ).email

    @validator("child_birthday", pre=True)
    def parse_child_birthday(cls, value):
        return datetime.strptime(value, "%d.%m.%Y").date()

    @validator("child_birthday")
    def validate_birthday(cls, value):
        if not date.today() > value > date.today() - timedelta(days=365 * 18):
            raise ValueError("Дата?")
        return value


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
    another_fund_help: Optional[str]

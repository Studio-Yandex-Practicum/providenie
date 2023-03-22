from datetime import date, datetime, timedelta
from typing import Optional

from email_validate import validate_or_fail
from pydantic import BaseModel, EmailStr, Field, validator

from bot.constants.info.text import REGEX_FULL_NAME, REGEX_PHONE


class BaseForm(BaseModel):
    """Base model for forms."""

    def __new__(cls):
        '''Method overriding makes it possible to change the order of
        the fields.
        All class.__fields__ must be specified in "fields_order"
        for correct method working if you need to change its ordering
        otherwise there is no need to define "fields_order" in Config.'''

        fields_order = cls.Config.__dict__.get('fields_order')
        if fields_order:
            fields = cls.__fields__
            cls.__fields__ = {key: fields.get(key) for key in fields_order}
        return super().__new__(cls)

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

    parent_full_name: str = Field(None, regex=REGEX_FULL_NAME, max_length=100)
    phone: str = Field(None, regex=REGEX_PHONE, strip_whitespace=True)
    email: Optional[EmailStr]
    child_full_name: str = Field(None, regex=REGEX_FULL_NAME, max_length=100)
    child_birthday: Optional[date]
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
    request_date: Optional[str]
    social_networks: Optional[str]
    parents_work_place: Optional[str]
    another_fund_member: Optional[str]

    class Config:
        fields_order = ['parent_full_name', 'phone', 'email', 'social_networks',
                        'child_full_name', 'child_birthday', 'family_members',
                        'address', 'city', 'child_birth_place', 'child_birth_date',
                        'child_birth_weight', 'child_birth_height', 'child_diagnosis',
                        'parents_work_place', 'request_date', 'where_got_info',
                        'required_therapy', 'request_goal', 'another_fund_member']

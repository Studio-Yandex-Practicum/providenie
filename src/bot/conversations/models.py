from datetime import date
from typing import Optional

from email_validator import validate_email
from pydantic import BaseModel, EmailStr, Field, validator

from bot.constants.info.text import REGEX_PHONE


class BaseForm(BaseModel):
    """Base model for forms."""

    class Config:
        min_anystr_length = 1
        max_anystr_length = 4096
        validate_assignment = True


class ShortForm(BaseForm):
    """Base model for short forms."""
    full_name: Optional[str]
    phone: str = Field(..., regex=REGEX_PHONE, strip_whitespace=True)
    email: Optional[EmailStr]

    @validator('email')
    def validator_email(email):
        return validate_email(
            email,
            check_deliverability=False,
        ).email


class VolunteerForm(ShortForm):
    """Model for volunteer form."""
    birthday: date = Field(
        ...,
        gt=date.today().year - 18,
        lt=date.today(),
    )
    city: Optional[str]
    volunteer_help: Optional[str]


class AskQuestionForm(ShortForm):
    """Model for 'Ask a question' form."""
    question: Optional[str]


class LongForm(BaseForm):
    """Base model for long forms."""
    parent_full_name: Optional[str]
    phone: str = Field(..., regex=REGEX_PHONE, strip_whitespace=True)
    child_full_name: Optional[str]
    child_birthday: Optional[str]
    child_birth_place: Optional[str]
    child_birth_date: int = Field(..., ge=22, le=37.)
    child_birth_weight: int = Field(..., ge=400, le=4000)
    child_birth_height: int = Field(..., ge=30, le=56)
    child_diagnosis: Optional[str]
    where_got_info: Optional[str]


class ChatForm(LongForm):
    """Model for chat application form."""
    operation: Optional[str]


class FundForm(LongForm):
    """Model for fund application form."""
    email: Optional[EmailStr]
    family_members: int = Field(..., ge=2)
    city: Optional[str]
    address: Optional[str]
    another_fund_member: Optional[str]
    another_fund_help: Optional[str]

    @ validator('email')
    def validator_email(email):
        return validate_email(
            email,
            check_deliverability=False,
        ).email

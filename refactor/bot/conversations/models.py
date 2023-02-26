from typing import Optional

from pydantic import BaseModel, EmailStr  # , validator, ValidationError


class BaseForm(BaseModel):
    """Base model for forms"""

    class Config:
        min_anystr_length = 1
        max_anystr_length = 4096
        validate_assignment = True


class ShortForm(BaseForm):
    """Base model for short forms"""

    full_name: Optional[int]
    phone: Optional[str]
    email: Optional[EmailStr]


class VolunteerForm(ShortForm):
    """Model for volunteer form"""

    birthday: Optional[str]
    city: Optional[str]
    volunteer_help: Optional[str]


class AskQuestionForm(ShortForm):
    """Model for 'Ask a question' form"""

    question: Optional[str]


class LongForm(BaseForm):
    """Base model for long forms"""

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


class ChatForm(LongForm):
    """Model for chat application form"""

    operation: Optional[str]


class FundForm(LongForm):
    """Model for fund application form"""

    email: Optional[EmailStr]
    family_members: Optional[int]
    city: Optional[str]
    address: Optional[str]
    another_fund_member: Optional[str]
    another_fund_help: Optional[str]

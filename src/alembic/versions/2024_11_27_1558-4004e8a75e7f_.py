"""empty message

Revision ID: 4004e8a75e7f
Revises: c04157089785
Create Date: 2024-11-27 15:58:23.928532

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4004e8a75e7f'
down_revision: Union[str, None] = 'c04157089785'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

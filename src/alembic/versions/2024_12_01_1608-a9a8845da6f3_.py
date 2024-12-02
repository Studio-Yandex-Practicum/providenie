"""empty message

Revision ID: a9a8845da6f3
Revises: 8549e518498b
Create Date: 2024-12-01 16:08:53.180021

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9a8845da6f3'
down_revision: Union[str, None] = '8549e518498b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
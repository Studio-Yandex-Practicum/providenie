"""empty message

Revision ID: f22b286f441e
Revises: 73ed88bf0ecc
Create Date: 2024-12-01 19:09:08.354558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f22b286f441e'
down_revision: Union[str, None] = '73ed88bf0ecc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
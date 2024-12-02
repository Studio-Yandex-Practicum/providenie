"""empty message

Revision ID: 8549e518498b
Revises: 7aefaacef381
Create Date: 2024-12-01 16:02:26.190503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8549e518498b'
down_revision: Union[str, None] = '7aefaacef381'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
"""empty message

Revision ID: 7788b310bee1
Revises: a9a8845da6f3
Create Date: 2024-12-01 17:36:10.452623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7788b310bee1'
down_revision: Union[str, None] = 'a9a8845da6f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
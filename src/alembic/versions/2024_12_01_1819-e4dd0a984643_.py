"""empty message

Revision ID: e4dd0a984643
Revises: 7788b310bee1
Create Date: 2024-12-01 18:19:25.618423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4dd0a984643'
down_revision: Union[str, None] = '7788b310bee1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
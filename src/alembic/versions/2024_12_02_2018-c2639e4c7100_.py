"""empty message

Revision ID: c2639e4c7100
Revises: f22b286f441e
Create Date: 2024-12-02 20:18:34.870336

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2639e4c7100'
down_revision: Union[str, None] = 'f22b286f441e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
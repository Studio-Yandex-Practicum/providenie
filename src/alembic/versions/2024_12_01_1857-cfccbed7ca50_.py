"""empty message

Revision ID: cfccbed7ca50
Revises: e4dd0a984643
Create Date: 2024-12-01 18:57:36.400213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfccbed7ca50'
down_revision: Union[str, None] = 'e4dd0a984643'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
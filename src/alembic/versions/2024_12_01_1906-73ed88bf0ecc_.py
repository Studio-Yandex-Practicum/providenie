"""empty message

Revision ID: 73ed88bf0ecc
Revises: cfccbed7ca50
Create Date: 2024-12-01 19:06:22.002019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73ed88bf0ecc'
down_revision: Union[str, None] = 'cfccbed7ca50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
"""Migrations change tg_id string to number

Revision ID: 0e3d1d822d4a
Revises: c04157089785
Create Date: 2024-11-21 10:32:39.221184

"""
from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e3d1d822d4a'
down_revision: Union[str, None] = 'c04157089785'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Приведение данных к Integer
    op.execute("UPDATE user_tg SET tg_id = NULL WHERE tg_id ~ '[^0-9]';")
    op.execute("UPDATE user_tg SET tg_id = CAST(tg_id AS INTEGER) WHERE tg_id IS NOT NULL;")
    
    # Изменение типа столбца
    op.alter_column('user_tg', 'tg_id',
                    existing_type=sa.VARCHAR(),
                    type_=sa.Integer(),
                    existing_nullable=False,
                    postgresql_using='tg_id::integer')

    op.alter_column('group', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('group_id_seq'::regclass)"))
    op.alter_column('message', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('message_id_seq'::regclass)"))
    op.alter_column('photo', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('user_group', 'user_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)
    op.alter_column('user_group', 'group_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)
    op.alter_column('user_group', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False)
    op.alter_column('user_tg', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('user_tg_id_seq'::regclass)"))


def downgrade() -> None:
    # Приведение данных обратно в строку
    op.execute("UPDATE user_tg SET tg_id = CAST(tg_id AS TEXT);")
    op.alter_column('user_tg', 'tg_id',
                    existing_type=sa.Integer(),
                    type_=sa.VARCHAR(),
                    existing_nullable=False)

    op.alter_column('user_tg', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('user_tg_id_seq'::regclass)"))
    op.alter_column('user_group', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
    op.alter_column('user_group', 'group_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
    op.alter_column('user_group', 'user_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False)
    op.alter_column('photo', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('message', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('message_id_seq'::regclass)"))
    op.alter_column('group', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('group_id_seq'::regclass)"))

"""add user table

Revision ID: fac63a1481f4
Revises: a498316807f3
Create Date: 2024-01-12 19:11:13.067410

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'fac63a1481f4'
down_revision: Union[str, None] = 'a498316807f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id',sa.Integer(),nullable=False),
    sa.Column('email',sa.String,nullable=False),
    sa.Column('password',sa.String(),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
    sa.PrimaryKeyConstraint('id'),sa.UniqueConstraint('email'))


def downgrade() -> None:
    op.drop_table('users')
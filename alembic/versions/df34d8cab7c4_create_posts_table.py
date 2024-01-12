"""create Posts table

Revision ID: df34d8cab7c4
Revises: 
Create Date: 2024-01-12 18:56:45.570477

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'df34d8cab7c4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
    sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')

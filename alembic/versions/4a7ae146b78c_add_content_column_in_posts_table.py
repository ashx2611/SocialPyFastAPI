"""add content column in  Posts table

Revision ID: 4a7ae146b78c
Revises: df34d8cab7c4
Create Date: 2024-01-12 19:07:14.132717

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4a7ae146b78c'
down_revision: Union[str, None] = 'df34d8cab7c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass

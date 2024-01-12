"""add columns to post

Revision ID: 3e95d4009115
Revises: 59345ac44eb6
Create Date: 2024-01-13 00:06:11.101940

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '3e95d4009115'
down_revision: Union[str, None] = '59345ac44eb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default=True),
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')),))


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    

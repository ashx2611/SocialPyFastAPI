"""add foreign key to post

Revision ID: 59345ac44eb6
Revises: fac63a1481f4
Create Date: 2024-01-12 23:52:44.984238

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '59345ac44eb6'
down_revision: Union[str, None] = 'fac63a1481f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table="posts",referent_table="users",
    local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')

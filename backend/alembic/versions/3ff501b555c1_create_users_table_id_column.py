"""Create users table id column

Revision ID: 3ff501b555c1
Revises: 3904ec7611bd
Create Date: 2025-12-03 10:08:31.202877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ff501b555c1'
down_revision: Union[str, Sequence[str], None] = '3904ec7611bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('id', sa.Integer(), primary_key=True, nullable=False))
    op.alter_column('users', 'username', primary_key=False, unique=True, nullable=False)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'username', primary_key=True, nullable=False)
    op.drop_column('users', 'id')
    pass

"""add active column to rotation_times table

Revision ID: d187b08d5a32
Revises: 1387264bb1ff
Create Date: 2025-12-15 21:59:21.374079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd187b08d5a32'
down_revision: Union[str, Sequence[str], None] = '1387264bb1ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('rotation_times', sa.Column('active', sa.Boolean(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('rotation_times', 'active')
    pass

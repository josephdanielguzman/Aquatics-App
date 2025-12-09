"""add boolean flag column to assignments table

Revision ID: 6331f7ff896b
Revises: 3ff501b555c1
Create Date: 2025-12-09 00:08:52.521917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6331f7ff896b'
down_revision: Union[str, Sequence[str], None] = '3ff501b555c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'assignments',
        sa.Column(
            'active',
            sa.Boolean(),
            nullable=False,
            default=True
        )
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('assignments', 'active')
    pass

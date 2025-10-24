"""set spot_id column of Assignments table to be nullable

Revision ID: 4a05fd348d60
Revises: c4cb81a5e2fa
Create Date: 2025-10-23 20:44:58.489759

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a05fd348d60'
down_revision: Union[str, Sequence[str], None] = 'c4cb81a5e2fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("assignments", "spot_id", nullable=True)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("assignments", "spot_id", nullable=False)
    pass

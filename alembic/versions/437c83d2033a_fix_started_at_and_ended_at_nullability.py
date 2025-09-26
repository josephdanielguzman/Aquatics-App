"""fix started_at and ended_at nullability

Revision ID: 437c83d2033a
Revises: d24d61681262
Create Date: 2025-09-25 21:58:40.179889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '437c83d2033a'
down_revision: Union[str, Sequence[str], None] = 'd24d61681262'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("shifts", "started_at", nullable=False)
    op.alter_column("shifts", "ended_at", nullable=True)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("shifts", "started_at", nullable=True)
    op.alter_column("shifts", "ended_at", nullable=False)
    pass

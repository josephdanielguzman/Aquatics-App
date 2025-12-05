"""create assignments table

Revision ID: d24d61681262
Revises: c5334052aa5c
Create Date: 2025-09-25 15:03:45.991257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd24d61681262'
down_revision: Union[str, Sequence[str], None] = 'c5334052aa5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("assignments",
                    sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("shift_id", sa.Integer, sa.ForeignKey("shifts.id"), nullable=False),
                    sa.Column("spot_id", sa.Integer, sa.ForeignKey("spots.id"), nullable=False),
                    sa.Column("time", sa.String, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("assignments")
    pass

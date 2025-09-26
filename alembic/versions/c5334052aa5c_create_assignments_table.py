"""create shifts table

Revision ID: c5334052aa5c
Revises: 0bda0bcbe9e0
Create Date: 2025-09-25 12:40:53.244696

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5334052aa5c'
down_revision: Union[str, Sequence[str], None] = '0bda0bcbe9e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("shifts",
                    sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("guard_id", sa.Integer, sa.ForeignKey("guards.id"), nullable = False),
                    sa.Column("started_at", sa.String, nullable=True),
                    sa.Column("ended_at", sa.String, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("shifts")
    pass
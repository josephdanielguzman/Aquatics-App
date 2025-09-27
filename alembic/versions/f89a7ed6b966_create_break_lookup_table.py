"""create break lookup table

Revision ID: f89a7ed6b966
Revises: 437c83d2033a
Create Date: 2025-09-26 23:28:16.002122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f89a7ed6b966'
down_revision: Union[str, Sequence[str], None] = '437c83d2033a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("break_types",
                    sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("type", sa.String, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("break_types")
    pass

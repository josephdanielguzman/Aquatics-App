"""create spots table

Revision ID: 0bda0bcbe9e0
Revises: b753ccb7a73f
Create Date: 2025-09-25 11:17:47.905904

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0bda0bcbe9e0'
down_revision: Union[str, Sequence[str], None] = 'b753ccb7a73f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("spots",
                    sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("rotation_id", sa.Integer, sa.ForeignKey("rotations.id"), nullable=False),
                    sa.Column("name", sa.String, nullable=False, unique=True),
                    sa.Column("order", sa.Integer, nullable=False),
                    sa.Column("is_active", sa.Boolean, nullable=False, default=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("spots")
    pass

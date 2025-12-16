"""create rotation_times table

Revision ID: 1387264bb1ff
Revises: 0d67347116c5
Create Date: 2025-12-15 21:30:10.666612

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1387264bb1ff'
down_revision: Union[str, Sequence[str], None] = '0d67347116c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('rotation_times',
                    sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("rotation_id", sa.Integer, sa.ForeignKey("rotations.id"), nullable=False),
                    sa.Column("time", sa.String, nullable=False)
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('rotation_times')
    pass

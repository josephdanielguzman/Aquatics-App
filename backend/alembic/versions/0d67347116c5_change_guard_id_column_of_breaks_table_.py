"""change guard_id column of Breaks table to shift_id

Revision ID: 0d67347116c5
Revises: 6331f7ff896b
Create Date: 2025-12-12 22:23:39.095597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d67347116c5'
down_revision: Union[str, Sequence[str], None] = '6331f7ff896b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('breaks', 'guard_id', new_column_name='shift_id')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('breaks', 'shift_id', new_column_name='guard_id')
    pass

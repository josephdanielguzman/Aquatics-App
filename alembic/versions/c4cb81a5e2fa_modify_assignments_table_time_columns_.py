"""modify assignments table time columns to be of type time instead of str

Revision ID: c4cb81a5e2fa
Revises: 072f192a3cc0
Create Date: 2025-10-16 12:52:53.473088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4cb81a5e2fa'
down_revision: Union[str, Sequence[str], None] = '072f192a3cc0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("assignments", "time",
                    type_=sa.Time(),
                    existing_type=sa.String(),
                    postgresql_using="TO_TIMESTAMP(time, 'HH:MI AM')::time")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("assignments", "time",
                    type_=sa.String(),
                    existing_type=sa.Time(),
                    postgresql_using="TO_CHAR(time, 'HH:MI AM')")
    pass

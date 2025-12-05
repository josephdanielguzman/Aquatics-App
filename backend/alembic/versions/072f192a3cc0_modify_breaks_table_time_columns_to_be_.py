"""modify breaks table time columns to be of type time instead of str

Revision ID: 072f192a3cc0
Revises: 740af435244c
Create Date: 2025-10-16 12:44:47.641224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '072f192a3cc0'
down_revision: Union[str, Sequence[str], None] = '740af435244c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("breaks", "start_time",
                    type_=sa.Time(),
                    existing_type=sa.String(),
                    postgresql_using="TO_TIMESTAMP(start_time, 'HH:MI AM')::time")
    op.alter_column("breaks", "end_time",
                    type_=sa.Time(),
                    existing_type=sa.String(),
                    postgresql_using="TO_TIMESTAMP(end_time, 'HH:MI AM')::time")
    pass

def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("shifts", "start_time",
                    type_=sa.String(),
                    existing_type=sa.Time(),
                    postgresql_using="TO_CHAR(start_time, 'HH:MI AM')")
    op.alter_column("shifts", "end_time",
                    type_=sa.String(),
                    existing_type=sa.Time(),
                    postgresql_using="TO_CHAR(end_time, 'HH:MI AM')")
    pass
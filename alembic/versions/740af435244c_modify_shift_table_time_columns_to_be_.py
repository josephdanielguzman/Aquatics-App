"""modify shift table time columns to be of type time instead of str

Revision ID: 740af435244c
Revises: 1be5866701de
Create Date: 2025-10-16 12:14:25.957671

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '740af435244c'
down_revision: Union[str, Sequence[str], None] = '1be5866701de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("shifts", "started_at",
                    type_=sa.Time(),
                    existing_type=sa.String(),
                    postgresql_using="TO_TIMESTAMP(started_at, 'HH:MI AM')::time")
    op.alter_column("shifts", "ended_at",
                    type_=sa.Time(),
                    existing_type=sa.String(),
                    postgresql_using="TO_TIMESTAMP(ended_at, 'HH:MI AM')::time")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("shifts", "started_at",
                    type_=sa.String(),
                    existing_type=sa.Time(),
                    postgresql_using="TO_CHAR(started_at, 'HH:MI AM')")
    op.alter_column("shifts", "ended_at",
                    type_=sa.String(),
                    existing_type=sa.Time(),
                    postgresql_using="TO_CHAR(ended_at, 'HH:MI AM')")
    pass

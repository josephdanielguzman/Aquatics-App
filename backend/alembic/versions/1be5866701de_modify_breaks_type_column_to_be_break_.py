"""drop breaks type column and replace with new type column of break_types foreign key

Revision ID: 1be5866701de
Revises: f89a7ed6b966
Create Date: 2025-09-26 23:35:10.628444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1be5866701de'
down_revision: Union[str, Sequence[str], None] = 'f89a7ed6b966'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("breaks", "type")
    op.add_column("breaks", sa.Column("type", sa.Integer, sa.ForeignKey("break_types.id"), nullable=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("breaks", "type")
    op.add_column("breaks", sa.Column("type", sa.String, nullable=False))

    pass

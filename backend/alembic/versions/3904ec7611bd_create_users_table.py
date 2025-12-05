"""create users table

Revision ID: 3904ec7611bd
Revises: 4a05fd348d60
Create Date: 2025-12-02 22:49:44.114629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3904ec7611bd'
down_revision: Union[str, Sequence[str], None] = '4a05fd348d60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users",
                    sa.Column("username",sa.String, primary_key=True, nullable=False),
                    sa.Column("password", sa.String, nullable=False))
    pass

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    pass

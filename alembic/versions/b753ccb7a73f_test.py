"""create the rotation reference table



Revision ID: b753ccb7a73f
Revises: 
Create Date: 2025-09-23 23:47:15.525696

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b753ccb7a73f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("rotations",
                    sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                             sa.Column("name", sa.String, nullable=False, unique=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("rotations")
    pass

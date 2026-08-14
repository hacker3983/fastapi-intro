"""Add a column

Revision ID: 0bd9c9e23133
Revises: 6f2ff7f01444
Create Date: 2026-08-06 15:41:43.652054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bd9c9e23133'
down_revision: Union[str, Sequence[str], None] = '6f2ff7f01444'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('account', sa.Column("last_transaction_date", sa.DateTime))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("account", "last_transaction_date")

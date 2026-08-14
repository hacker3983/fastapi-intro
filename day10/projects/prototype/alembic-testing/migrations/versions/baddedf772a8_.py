"""empty message

Revision ID: baddedf772a8
Revises: 77a072e5fa34
Create Date: 2026-08-06 16:33:33.491529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'baddedf772a8'
down_revision: Union[str, Sequence[str], None] = '77a072e5fa34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

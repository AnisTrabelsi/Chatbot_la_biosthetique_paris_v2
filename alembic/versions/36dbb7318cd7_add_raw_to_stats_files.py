"""add raw to stats_files

Revision ID: 36dbb7318cd7
Revises: dc26a0e494f0
Create Date: 2025-06-11 18:08:21.195074

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36dbb7318cd7'
down_revision: Union[str, None] = 'dc26a0e494f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

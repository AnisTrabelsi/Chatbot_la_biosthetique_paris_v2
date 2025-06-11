"""add raw to stats_files (tests)

Revision ID: a1e7de626fad
Revises: 36dbb7318cd7
Create Date: 2025-06-11 18:15:51.153207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1e7de626fad'
down_revision: Union[str, None] = '36dbb7318cd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

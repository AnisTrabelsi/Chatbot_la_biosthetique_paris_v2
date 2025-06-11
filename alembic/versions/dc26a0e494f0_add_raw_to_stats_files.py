"""add raw to stats_files

Revision ID: dc26a0e494f0
Revises: be605faa94dd
Create Date: 2025-06-11 18:02:31.368187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc26a0e494f0'
down_revision: Union[str, None] = 'be605faa94dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

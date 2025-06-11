"""add raw column to stats_files

Revision ID: be605faa94dd
Revises: 01d971d5312e
Create Date: 2025-06-11 17:15:52.922608

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be605faa94dd'
down_revision: Union[str, None] = '01d971d5312e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

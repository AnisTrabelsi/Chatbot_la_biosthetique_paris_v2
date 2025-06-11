"""Add owner_id to client

Revision ID: 01d971d5312e
Revises: 23d096f078fc
Create Date: 2025-06-11 16:00:44.280020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01d971d5312e'
down_revision: Union[str, None] = '23d096f078fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

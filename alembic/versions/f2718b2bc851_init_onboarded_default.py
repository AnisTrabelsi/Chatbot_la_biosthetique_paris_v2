"""Init onboarded default

Revision ID: f2718b2bc851
Revises: d2d38e95898c
Create Date: 2025-06-11 14:52:59.513385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2718b2bc851'
down_revision: Union[str, None] = 'd2d38e95898c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

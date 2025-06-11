"""Add phone_e164 kdnr siret to clients

Revision ID: bb95a298f7e2
Revises: f2718b2bc851
Create Date: 2025-06-11 15:42:54.034284

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb95a298f7e2'
down_revision: Union[str, None] = 'f2718b2bc851'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

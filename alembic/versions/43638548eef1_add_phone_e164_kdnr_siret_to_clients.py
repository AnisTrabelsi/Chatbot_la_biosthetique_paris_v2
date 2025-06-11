"""Add phone_e164 kdnr siret to clients

Revision ID: 43638548eef1
Revises: bb95a298f7e2
Create Date: 2025-06-11 15:43:40.412289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43638548eef1'
down_revision: Union[str, None] = 'bb95a298f7e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

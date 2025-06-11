"""Add user_id to wa_sessions

Revision ID: ef3d7a49b357
Revises: a1e7de626fad
Create Date: 2025-06-11 18:21:12.623324

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef3d7a49b357'
down_revision: Union[str, None] = 'a1e7de626fad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

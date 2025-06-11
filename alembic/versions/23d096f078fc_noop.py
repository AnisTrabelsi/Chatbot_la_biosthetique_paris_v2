"""noop

Revision ID: 23d096f078fc
Revises: 43638548eef1
Create Date: 2025-06-11 15:48:51.874400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23d096f078fc'
down_revision: Union[str, None] = '43638548eef1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

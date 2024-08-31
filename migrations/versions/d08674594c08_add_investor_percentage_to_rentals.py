"""ADD 'investor_percentage' to rentals

Revision ID: d08674594c08
Revises: 5bc84ddc3f9f
Create Date: 2024-08-31 21:51:54.943451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd08674594c08'
down_revision: Union[str, None] = '5bc84ddc3f9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("rentals", sa.Column("investor_percentage", sa.Float))


def downgrade() -> None:
    op.drop_column("rentals", "investor_percentage")

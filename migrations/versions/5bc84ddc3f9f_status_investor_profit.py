"""status & investor_profit

Revision ID: 5bc84ddc3f9f
Revises: 126f4e6c2868
Create Date: 2024-08-30 23:20:38.925717

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bc84ddc3f9f'
down_revision: Union[str, None] = '126f4e6c2868'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('rentals', sa.Column('investor_profit', sa.Integer(), nullable=True))
    op.add_column('rentals', sa.Column('status', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('rentals', 'investor_profit')
    op.drop_column('rentals', 'status')

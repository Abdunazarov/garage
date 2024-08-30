"""ADD all tables

Revision ID: 0f7b23f8bc49
Revises: 
Create Date: 2024-08-30 14:09:53.033689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f7b23f8bc49'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('renters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('car_name', sa.String(), nullable=False),
    sa.Column('owner_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rentals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('renter_id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.Column('issue_date', sa.Date(), nullable=False),
    sa.Column('return_date', sa.Date(), nullable=False),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.Column('payment_method', sa.String(), nullable=False),
    sa.Column('deposit', sa.Float(), nullable=False),
    sa.Column('mileage', sa.Float(), nullable=True),
    sa.Column('fuel_cost', sa.Float(), nullable=True),
    sa.Column('other_expenses', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['car_id'], ['cars.id'], ),
    sa.ForeignKeyConstraint(['renter_id'], ['renters.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('rentals')
    op.drop_table('cars')
    op.drop_table('renters')

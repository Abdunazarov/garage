"""ADD 'users'

Revision ID: 126f4e6c2868
Revises: 0f7b23f8bc49
Create Date: 2024-08-30 15:14:21.718134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from passlib.hash import bcrypt
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = '126f4e6c2868'
down_revision: Union[str, None] = '0f7b23f8bc49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('phone_number', sa.String, nullable=False),
        sa.Column('is_admin', sa.Boolean),
        sa.Column('hashed_password', sa.String, nullable=False)
    )

    op.execute(
        text(
            """
        INSERT INTO users (username, name, phone_number, is_admin, hashed_password)
        VALUES ('super_admin', 'Garage Admin', '+99897 777-77-77', TRUE, :hashed_password)
    """
        ).bindparams(
            hashed_password=bcrypt.hash("garage_super_admin")
        )
    )

def downgrade():
    op.drop_table('users')

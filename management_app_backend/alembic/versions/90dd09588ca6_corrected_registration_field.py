"""Corrected registration field

Revision ID: 90dd09588ca6
Revises: 8286d06f0db4
Create Date: 2023-01-03 01:06:45.608116

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '90dd09588ca6'
down_revision = '8286d06f0db4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('registration_date', sa.DateTime(), nullable=True))
    op.drop_column('users', 'resgistration_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('resgistration_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('users', 'registration_date')
    # ### end Alembic commands ###

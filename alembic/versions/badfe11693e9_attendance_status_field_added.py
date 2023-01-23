"""Attendance Status Field Added

Revision ID: badfe11693e9
Revises: 5e44b630c171
Create Date: 2023-01-23 11:07:56.112790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'badfe11693e9'
down_revision = '5e44b630c171'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('staffattendance', sa.Column(
        'status', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('staffattendance', 'status')
    # ### end Alembic commands ###
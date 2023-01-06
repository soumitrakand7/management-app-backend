"""Added Subscription Plans

Revision ID: 00ab69b14f5a
Revises: 82ccbad1d71f
Create Date: 2023-01-02 16:19:37.976839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00ab69b14f5a'
down_revision = '82ccbad1d71f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscriptionplan',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('members', sa.Float(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscriptionplan')
    # ### end Alembic commands ###
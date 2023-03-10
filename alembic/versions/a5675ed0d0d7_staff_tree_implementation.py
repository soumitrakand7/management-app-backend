"""Staff Tree implementation

Revision ID: a5675ed0d0d7
Revises: 94181ec956dd
Create Date: 2023-02-09 01:29:05.709596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5675ed0d0d7'
down_revision = '94181ec956dd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stafftree',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('staff_id', sa.String(length=36), nullable=True),
    sa.Column('senior_staff_id', sa.String(length=36), nullable=True),
    sa.Column('relation_tag', sa.String(length=24), nullable=False),
    sa.Column('subscriber_group_id', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['senior_staff_id'], ['staffmember.id'], ),
    sa.ForeignKeyConstraint(['staff_id'], ['staffmember.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stafftree')
    # ### end Alembic commands ###

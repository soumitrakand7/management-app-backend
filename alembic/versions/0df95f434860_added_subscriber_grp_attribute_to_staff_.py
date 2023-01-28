"""Added Subscriber Grp attribute to Staff Tasks

Revision ID: 0df95f434860
Revises: a0afa5c951cb
Create Date: 2023-01-28 21:03:27.835384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0df95f434860'
down_revision = 'a0afa5c951cb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stafftask', sa.Column('subscriber_group_id', sa.String(length=36), nullable=True))
    op.create_foreign_key(None, 'stafftask', 'subscribergroup', ['subscriber_group_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'stafftask', type_='foreignkey')
    op.drop_column('stafftask', 'subscriber_group_id')
    # ### end Alembic commands ###
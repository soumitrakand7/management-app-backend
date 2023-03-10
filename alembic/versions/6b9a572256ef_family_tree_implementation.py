"""Family Tree Implementation

Revision ID: 6b9a572256ef
Revises: c0c9b18ddb29
Create Date: 2023-01-14 08:37:10.304772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b9a572256ef'
down_revision = 'c0c9b18ddb29'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('familymember', sa.Column('child_email', sa.String(length=36), nullable=False))
    op.add_column('familymember', sa.Column('first_parent_email', sa.String(length=36), nullable=True))
    op.add_column('familymember', sa.Column('second_parent_email', sa.String(length=36), nullable=True))
    op.add_column('familymember', sa.Column('subscriber_group_id', sa.String(length=36), nullable=False))
    op.drop_index('ix_familymember_relation_tag', table_name='familymember')
    op.drop_constraint('familymember_user_email_fkey', 'familymember', type_='foreignkey')
    op.create_foreign_key(None, 'familymember', 'users', ['first_parent_email'], ['email'])
    op.create_foreign_key(None, 'familymember', 'users', ['second_parent_email'], ['email'])
    op.create_foreign_key(None, 'familymember', 'users', ['child_email'], ['email'])
    op.drop_column('familymember', 'relation_tag')
    op.drop_column('familymember', 'user_email')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('familymember', sa.Column('user_email', sa.VARCHAR(length=32), autoincrement=False, nullable=True))
    op.add_column('familymember', sa.Column('relation_tag', sa.VARCHAR(length=24), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'familymember', type_='foreignkey')
    op.drop_constraint(None, 'familymember', type_='foreignkey')
    op.drop_constraint(None, 'familymember', type_='foreignkey')
    op.create_foreign_key('familymember_user_email_fkey', 'familymember', 'users', ['user_email'], ['email'])
    op.create_index('ix_familymember_relation_tag', 'familymember', ['relation_tag'], unique=False)
    op.drop_column('familymember', 'subscriber_group_id')
    op.drop_column('familymember', 'second_parent_email')
    op.drop_column('familymember', 'first_parent_email')
    op.drop_column('familymember', 'child_email')
    # ### end Alembic commands ###

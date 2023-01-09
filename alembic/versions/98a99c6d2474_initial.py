"""Initial

Revision ID: 98a99c6d2474
Revises: 
Create Date: 2023-01-09 18:11:52.421905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98a99c6d2474'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscriptionplan',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('plan_name', sa.String(length=36), nullable=False),
    sa.Column('min_members', sa.Float(), nullable=True),
    sa.Column('max_members', sa.Float(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('email', sa.String(length=32), nullable=False),
    sa.Column('full_name', sa.String(length=64), nullable=False),
    sa.Column('mobile_no', sa.String(length=10), nullable=False),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('hashed_password', sa.String(length=512), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('profile_image_url', sa.Text(), nullable=True),
    sa.Column('activation_code', sa.Float(), nullable=True),
    sa.Column('registration_date', sa.DateTime(), nullable=True),
    sa.Column('profile', sa.String(length=36), nullable=True),
    sa.PrimaryKeyConstraint('email')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_full_name'), 'users', ['full_name'], unique=False)
    op.create_index(op.f('ix_users_mobile_no'), 'users', ['mobile_no'], unique=False)
    op.create_index(op.f('ix_users_profile'), 'users', ['profile'], unique=False)
    op.create_table('familymember',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('relation_tag', sa.String(length=24), nullable=False),
    sa.Column('user_email', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['user_email'], ['users.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_familymember_relation_tag'), 'familymember', ['relation_tag'], unique=False)
    op.create_table('guestmember',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_email', sa.String(length=32), nullable=True),
    sa.Column('relation_tag', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['user_email'], ['users.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_guestmember_relation_tag'), 'guestmember', ['relation_tag'], unique=False)
    op.create_table('staffmember',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_email', sa.String(length=36), nullable=True),
    sa.Column('designation', sa.String(length=24), nullable=False),
    sa.Column('job_details', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_email'], ['users.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_staffmember_designation'), 'staffmember', ['designation'], unique=False)
    op.create_table('subscribergroup',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('admin', sa.String(length=36), nullable=True),
    sa.Column('plan_id', sa.String(length=36), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('valid_until', sa.DateTime(), nullable=False),
    sa.Column('member_count', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['admin'], ['users.email'], ),
    sa.ForeignKeyConstraint(['plan_id'], ['subscriptionplan.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscribergroup_member_count'), 'subscribergroup', ['member_count'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_subscribergroup_member_count'), table_name='subscribergroup')
    op.drop_table('subscribergroup')
    op.drop_index(op.f('ix_staffmember_designation'), table_name='staffmember')
    op.drop_table('staffmember')
    op.drop_index(op.f('ix_guestmember_relation_tag'), table_name='guestmember')
    op.drop_table('guestmember')
    op.drop_index(op.f('ix_familymember_relation_tag'), table_name='familymember')
    op.drop_table('familymember')
    op.drop_index(op.f('ix_users_profile'), table_name='users')
    op.drop_index(op.f('ix_users_mobile_no'), table_name='users')
    op.drop_index(op.f('ix_users_full_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('subscriptionplan')
    # ### end Alembic commands ###

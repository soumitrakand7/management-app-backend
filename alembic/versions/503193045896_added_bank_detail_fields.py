"""Added bank detail fields

Revision ID: 503193045896
Revises: 758320eafb48
Create Date: 2023-01-20 13:56:43.741393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '503193045896'
down_revision = '758320eafb48'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('familymember', sa.Column('relation_tag', sa.String(length=32), nullable=True))
    op.create_index(op.f('ix_familymember_relation_tag'), 'familymember', ['relation_tag'], unique=False)
    op.add_column('users', sa.Column('bank_ifsc', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('bank_account_no', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'bank_account_no')
    op.drop_column('users', 'bank_ifsc')
    op.drop_index(op.f('ix_familymember_relation_tag'), table_name='familymember')
    op.drop_column('familymember', 'relation_tag')
    # ### end Alembic commands ###

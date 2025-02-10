"""add organisation entity

Revision ID: e329ffeec604
Revises: 76864ec11645
Create Date: 2025-02-10 09:52:01.453705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e329ffeec604'
down_revision = '76864ec11645'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('organisation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('entity', sa.BigInteger(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('organisation', schema=None) as batch_op:
        batch_op.drop_column('entity')

    # ### end Alembic commands ###

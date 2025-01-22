"""add dataset and record fields

Revision ID: 01fb7b23bc27
Revises: ff4030c2058a
Create Date: 2025-01-22 14:04:37.122668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01fb7b23bc27'
down_revision = 'ff4030c2058a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dataset', schema=None) as batch_op:
        batch_op.add_column(sa.Column('entity_minimum', sa.BigInteger(), nullable=True))
        batch_op.add_column(sa.Column('entity_maximum', sa.BigInteger(), nullable=True))

    with op.batch_alter_table('record', schema=None) as batch_op:
        batch_op.add_column(sa.Column('entity', sa.BigInteger(), nullable=True))
        batch_op.add_column(sa.Column('reference', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('notes', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('record', schema=None) as batch_op:
        batch_op.drop_column('notes')
        batch_op.drop_column('description')
        batch_op.drop_column('reference')
        batch_op.drop_column('entity')

    with op.batch_alter_table('dataset', schema=None) as batch_op:
        batch_op.drop_column('entity_maximum')
        batch_op.drop_column('entity_minimum')

    # ### end Alembic commands ###

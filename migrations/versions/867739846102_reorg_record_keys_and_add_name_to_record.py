"""reorg record keys and add name to record

Revision ID: 867739846102
Revises: 27248d969c76
Create Date: 2025-01-27 12:22:03.938293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '867739846102'
down_revision = '27248d969c76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('record', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.Text(), nullable=False))
        batch_op.alter_column('reference',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('record', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.UUID(), autoincrement=False, nullable=False))
        batch_op.alter_column('reference',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.drop_column('name')

    # ### end Alembic commands ###

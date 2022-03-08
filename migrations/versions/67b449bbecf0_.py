"""empty message

Revision ID: 67b449bbecf0
Revises: 472ead25b013
Create Date: 2022-02-21 12:54:27.247333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67b449bbecf0'
down_revision = '472ead25b013'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('access', schema=None) as batch_op:
        batch_op.drop_index('ix_access_name')
        batch_op.create_index(batch_op.f('ix_access_name'), ['name'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('access', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_access_name'))
        batch_op.create_index('ix_access_name', ['name'], unique=False)

    # ### end Alembic commands ###
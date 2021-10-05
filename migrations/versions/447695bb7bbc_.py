"""empty message

Revision ID: 447695bb7bbc
Revises: 16a87da24446
Create Date: 2021-10-05 15:51:47.060920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '447695bb7bbc'
down_revision = '16a87da24446'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('visitor_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('ip_address', sa.String(length=120), nullable=True),
    sa.Column('country', sa.String(length=10), nullable=True),
    sa.Column('region', sa.String(length=120), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('lat', sa.String(length=120), nullable=True),
    sa.Column('lng', sa.String(length=120), nullable=True),
    sa.Column('postalcode', sa.String(length=120), nullable=True),
    sa.Column('geonameid', sa.String(length=120), nullable=True),
    sa.Column('connectionType', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_visitor_log'))
    )
    with op.batch_alter_table('visitor_log', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_visitor_log_city'), ['city'], unique=False)
        batch_op.create_index(batch_op.f('ix_visitor_log_connectionType'), ['connectionType'], unique=False)
        batch_op.create_index(batch_op.f('ix_visitor_log_country'), ['country'], unique=False)
        batch_op.create_index(batch_op.f('ix_visitor_log_geonameid'), ['geonameid'], unique=False)
        batch_op.create_index(batch_op.f('ix_visitor_log_ip_address'), ['ip_address'], unique=False)
        batch_op.create_index(batch_op.f('ix_visitor_log_lat'), ['lat'], unique=False)
        batch_op.create_index(batch_op.f('ix_visitor_log_lng'), ['lng'], unique=False)
        batch_op.create_index(batch_op.f('ix_visitor_log_postalcode'), ['postalcode'], unique=False)
        batch_op.create_index(batch_op.f('ix_visitor_log_region'), ['region'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('visitor_log', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_visitor_log_region'))
        batch_op.drop_index(batch_op.f('ix_visitor_log_postalcode'))
        batch_op.drop_index(batch_op.f('ix_visitor_log_lng'))
        batch_op.drop_index(batch_op.f('ix_visitor_log_lat'))
        batch_op.drop_index(batch_op.f('ix_visitor_log_ip_address'))
        batch_op.drop_index(batch_op.f('ix_visitor_log_geonameid'))
        batch_op.drop_index(batch_op.f('ix_visitor_log_country'))
        batch_op.drop_index(batch_op.f('ix_visitor_log_connectionType'))
        batch_op.drop_index(batch_op.f('ix_visitor_log_city'))

    op.drop_table('visitor_log')
    # ### end Alembic commands ###

"""empty message

Revision ID: 81ad56f2b820
Revises: 
Create Date: 2022-02-13 20:48:20.342012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81ad56f2b820'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('slug', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_category'))
    )
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_category_name'), ['name'], unique=True)
        batch_op.create_index(batch_op.f('ix_category_slug'), ['slug'], unique=True)

    op.create_table('database',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('is_activated', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_database'))
    )
    with op.batch_alter_table('database', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_database_name'), ['name'], unique=False)

    op.create_table('feature_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_feature_category'))
    )
    with op.batch_alter_table('feature_category', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_feature_category_title'), ['title'], unique=False)

    op.create_table('lead',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fname', sa.String(length=128), nullable=True),
    sa.Column('lname', sa.String(length=128), nullable=True),
    sa.Column('orgname', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('utm_source', sa.String(length=128), nullable=True),
    sa.Column('utm_medium', sa.String(length=128), nullable=True),
    sa.Column('utm_campaign', sa.String(length=128), nullable=True),
    sa.Column('details', sa.Text(), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_lead'))
    )
    with op.batch_alter_table('lead', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_lead_details'), ['details'], unique=False)
        batch_op.create_index(batch_op.f('ix_lead_email'), ['email'], unique=False)
        batch_op.create_index(batch_op.f('ix_lead_fname'), ['fname'], unique=False)
        batch_op.create_index(batch_op.f('ix_lead_lname'), ['lname'], unique=False)
        batch_op.create_index(batch_op.f('ix_lead_orgname'), ['orgname'], unique=False)
        batch_op.create_index(batch_op.f('ix_lead_utm_campaign'), ['utm_campaign'], unique=False)
        batch_op.create_index(batch_op.f('ix_lead_utm_medium'), ['utm_medium'], unique=False)
        batch_op.create_index(batch_op.f('ix_lead_utm_source'), ['utm_source'], unique=False)

    op.create_table('model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_model'))
    )
    with op.batch_alter_table('model', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_model_name'), ['name'], unique=False)

    op.create_table('module_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_module_category'))
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('is_staff', sa.Boolean(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('registered_on', sa.DateTime(), nullable=True),
    sa.Column('phone_no', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('country_code', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_country_code'), ['country_code'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_phone_no'), ['phone_no'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_token'), ['token'], unique=True)

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
    sa.Column('timezone', sa.String(length=120), nullable=True),
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
        batch_op.create_index(batch_op.f('ix_visitor_log_timezone'), ['timezone'], unique=False)

    op.create_table('access',
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('model_id', sa.Integer(), nullable=True),
    sa.Column('read', sa.Boolean(), nullable=True),
    sa.Column('write', sa.Boolean(), nullable=True),
    sa.Column('create', sa.Boolean(), nullable=True),
    sa.Column('delete', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['model_id'], ['model.id'], name=op.f('fk_access_model_id_model')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_access'))
    )
    with op.batch_alter_table('access', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_access_name'), ['name'], unique=True)

    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('domain_name', sa.String(length=120), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('registered_on', sa.DateTime(), nullable=True),
    sa.Column('database_id', sa.Integer(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['database_id'], ['database.id'], name=op.f('fk_company_database_id_database')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_company_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_company'))
    )
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_company_domain_name'), ['domain_name'], unique=True)
        batch_op.create_index(batch_op.f('ix_company_name'), ['name'], unique=False)

    op.create_table('module',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('technical_name', sa.String(length=128), nullable=True),
    sa.Column('bp_name', sa.String(length=128), nullable=True),
    sa.Column('official_name', sa.String(length=128), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('author', sa.String(length=60), nullable=True),
    sa.Column('url', sa.String(length=120), nullable=True),
    sa.Column('latest_version', sa.String(length=60), nullable=True),
    sa.Column('published_version', sa.String(length=60), nullable=True),
    sa.Column('icon', sa.String(length=60), nullable=True),
    sa.Column('enable', sa.Boolean(), nullable=True),
    sa.Column('summary', sa.String(length=350), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['module_category.id'], name=op.f('fk_module_category_id_module_category')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_module'))
    )
    with op.batch_alter_table('module', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_module_bp_name'), ['bp_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_module_official_name'), ['official_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_module_technical_name'), ['technical_name'], unique=False)

    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('body_html', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('is_featured', sa.Boolean(), nullable=True),
    sa.Column('image_url', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], name=op.f('fk_post_author_id_user')),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], name=op.f('fk_post_category_id_category')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_post'))
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_post_timestamp'), ['timestamp'], unique=False)
        batch_op.create_index(batch_op.f('ix_post_title'), ['title'], unique=True)

    op.create_table('task',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.Column('user_redirected', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_task_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_task'))
    )
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_task_name'), ['name'], unique=False)

    op.create_table('company_modules',
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('module_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], name=op.f('fk_company_modules_company_id_company')),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], name=op.f('fk_company_modules_module_id_module')),
    sa.PrimaryKeyConstraint('company_id', 'module_id', name=op.f('pk_company_modules'))
    )
    op.create_table('group',
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('module_id', sa.Integer(), nullable=True),
    sa.Column('permission', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], name=op.f('fk_group_module_id_module')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_group'))
    )
    with op.batch_alter_table('group', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_group_name'), ['name'], unique=False)

    op.create_table('module_feature',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('feature_category', sa.Integer(), nullable=True),
    sa.Column('module_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['feature_category'], ['feature_category.id'], name=op.f('fk_module_feature_feature_category_feature_category')),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], name=op.f('fk_module_feature_module_id_module')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_module_feature'))
    )
    with op.batch_alter_table('module_feature', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_module_feature_name'), ['name'], unique=False)

    op.create_table('AccessRights',
    sa.Column('group_id', sa.String(length=128), nullable=False),
    sa.Column('access_id', sa.String(length=128), nullable=False),
    sa.ForeignKeyConstraint(['access_id'], ['access.id'], name=op.f('fk_AccessRights_access_id_access')),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], name=op.f('fk_AccessRights_group_id_group')),
    sa.PrimaryKeyConstraint('group_id', 'access_id', name=op.f('pk_AccessRights'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('AccessRights')
    with op.batch_alter_table('module_feature', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_module_feature_name'))

    op.drop_table('module_feature')
    with op.batch_alter_table('group', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_group_name'))

    op.drop_table('group')
    op.drop_table('company_modules')
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_task_name'))

    op.drop_table('task')
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_title'))
        batch_op.drop_index(batch_op.f('ix_post_timestamp'))

    op.drop_table('post')
    with op.batch_alter_table('module', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_module_technical_name'))
        batch_op.drop_index(batch_op.f('ix_module_official_name'))
        batch_op.drop_index(batch_op.f('ix_module_bp_name'))

    op.drop_table('module')
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_company_name'))
        batch_op.drop_index(batch_op.f('ix_company_domain_name'))

    op.drop_table('company')
    with op.batch_alter_table('access', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_access_name'))

    op.drop_table('access')
    with op.batch_alter_table('visitor_log', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_visitor_log_timezone'))
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
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_token'))
        batch_op.drop_index(batch_op.f('ix_user_phone_no'))
        batch_op.drop_index(batch_op.f('ix_user_name'))
        batch_op.drop_index(batch_op.f('ix_user_email'))
        batch_op.drop_index(batch_op.f('ix_user_country_code'))

    op.drop_table('user')
    op.drop_table('module_category')
    with op.batch_alter_table('model', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_model_name'))

    op.drop_table('model')
    with op.batch_alter_table('lead', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_lead_utm_source'))
        batch_op.drop_index(batch_op.f('ix_lead_utm_medium'))
        batch_op.drop_index(batch_op.f('ix_lead_utm_campaign'))
        batch_op.drop_index(batch_op.f('ix_lead_orgname'))
        batch_op.drop_index(batch_op.f('ix_lead_lname'))
        batch_op.drop_index(batch_op.f('ix_lead_fname'))
        batch_op.drop_index(batch_op.f('ix_lead_email'))
        batch_op.drop_index(batch_op.f('ix_lead_details'))

    op.drop_table('lead')
    with op.batch_alter_table('feature_category', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_feature_category_title'))

    op.drop_table('feature_category')
    with op.batch_alter_table('database', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_database_name'))

    op.drop_table('database')
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_category_slug'))
        batch_op.drop_index(batch_op.f('ix_category_name'))

    op.drop_table('category')
    # ### end Alembic commands ###
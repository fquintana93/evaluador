"""empty message

Revision ID: 5f694ae59c93
Revises: 521f06b58769
Create Date: 2021-06-10 13:02:09.628077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f694ae59c93'
down_revision = '521f06b58769'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('lastname', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('empresa', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_admin'))
    )
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_admin_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_admin_username'), ['username'], unique=True)

    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('lastname', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('empresa_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['empresa_id'], ['admin.id'], name=op.f('fk_user_empresa_id_admin')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('consultas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rut', sa.String(length=20), nullable=True),
    sa.Column('cliente', sa.String(length=20), nullable=True),
    sa.Column('fecha_ev', sa.DateTime(), nullable=True),
    sa.Column('monto_linea', sa.String(length=50), nullable=True),
    sa.Column('adicional', sa.String(length=50), nullable=True),
    sa.Column('solicitudes', sa.String(length=10), nullable=True),
    sa.Column('aprobados', sa.String(length=10), nullable=True),
    sa.Column('empleados', sa.String(length=30), nullable=True),
    sa.Column('hipotecario', sa.String(length=50), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('cmf_deuda', sa.Float(), nullable=True),
    sa.Column('cmf_cupo', sa.Float(), nullable=True),
    sa.Column('cmf_mora', sa.Float(), nullable=True),
    sa.Column('cmf_instituciones', sa.Float(), nullable=True),
    sa.Column('iva_total_ventas', sa.Float(), nullable=True),
    sa.Column('iva_impuesto_renta', sa.Float(), nullable=True),
    sa.Column('iva_total_compras', sa.Float(), nullable=True),
    sa.Column('sii_empleados', sa.Integer(), nullable=True),
    sa.Column('sii_tramo_ventas', sa.String(length=50), nullable=True),
    sa.Column('sii_inicio_act', sa.String(length=50), nullable=True),
    sa.Column('sii_rubro', sa.String(length=200), nullable=True),
    sa.Column('sii_comuna', sa.String(length=50), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('empresa_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['empresa_id'], ['admin.id'], name=op.f('fk_consultas_empresa_id_admin')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_consultas_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_consultas'))
    )
    with op.batch_alter_table('consultas', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_consultas_fecha_ev'), ['fecha_ev'], unique=False)

    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_post_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_post'))
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_post_timestamp'), ['timestamp'], unique=False)

    with op.batch_alter_table('empresa', schema=None) as batch_op:
        batch_op.drop_index('ix_empresa_email')
        batch_op.drop_index('ix_empresa_username')

    op.drop_table('empresa')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('empresa',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=True),
    sa.Column('lastname', sa.VARCHAR(length=64), nullable=True),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('empresa', sa.VARCHAR(length=100), nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_empresa')
    )
    with op.batch_alter_table('empresa', schema=None) as batch_op:
        batch_op.create_index('ix_empresa_username', ['username'], unique=False)
        batch_op.create_index('ix_empresa_email', ['email'], unique=False)

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_timestamp'))

    op.drop_table('post')
    with op.batch_alter_table('consultas', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_consultas_fecha_ev'))

    op.drop_table('consultas')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_admin_username'))
        batch_op.drop_index(batch_op.f('ix_admin_email'))

    op.drop_table('admin')
    # ### end Alembic commands ###

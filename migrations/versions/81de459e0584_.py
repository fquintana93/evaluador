"""empty message

Revision ID: 81de459e0584
Revises: 81fa74b0cc64
Create Date: 2021-06-09 11:25:46.030347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81de459e0584'
down_revision = '81fa74b0cc64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_consultas_fecha_ev'), 'consultas', ['fecha_ev'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_consultas_fecha_ev'), table_name='consultas')
    op.drop_table('consultas')
    # ### end Alembic commands ###

"""empty message

Revision ID: cbf7228e5d40
Revises: 39b828c5a23e
Create Date: 2021-06-10 22:13:57.801823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbf7228e5d40'
down_revision = '39b828c5a23e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sii',
    sa.Column('rut', sa.String(length=20), nullable=False),
    sa.Column('tramoventas', sa.Integer(), nullable=True),
    sa.Column('trabajadores', sa.Integer(), nullable=True),
    sa.Column('inicio', sa.String(length=20), nullable=True),
    sa.Column('rubro', sa.String(length=200), nullable=True),
    sa.Column('comuna', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('rut', name=op.f('pk_sii'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sii')
    # ### end Alembic commands ###

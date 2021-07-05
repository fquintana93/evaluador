"""empty message

Revision ID: 58b33f790c3b
Revises: 9aa6b84bee94
Create Date: 2021-06-10 22:01:36.899637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58b33f790c3b'
down_revision = '9aa6b84bee94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sii',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rut', sa.String(length=20), nullable=False),
    sa.Column('tramoventas', sa.Integer(), nullable=True),
    sa.Column('trabajadores', sa.Integer(), nullable=True),
    sa.Column('inicio', sa.String(length=20), nullable=True),
    sa.Column('rubro', sa.String(length=200), nullable=True),
    sa.Column('comuna', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id', 'rut', name=op.f('pk_sii'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sii')
    # ### end Alembic commands ###
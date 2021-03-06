"""empty message

Revision ID: faacf5517ab9
Revises: bd76b925c12e
Create Date: 2021-06-23 15:38:17.843550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'faacf5517ab9'
down_revision = 'bd76b925c12e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('consultas', sa.Column('antiguedad_cli', sa.Integer(), nullable=True))
    op.add_column('consultas', sa.Column('cupoAprobado', sa.Integer(), nullable=True))
    op.add_column('consultas', sa.Column('cupoUtilizado', sa.Integer(), nullable=True))
    op.add_column('consultas', sa.Column('nVentas', sa.Integer(), nullable=True))
    op.add_column('consultas', sa.Column('incumplimientos', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('consultas', 'incumplimientos')
    op.drop_column('consultas', 'nVentas')
    op.drop_column('consultas', 'cupoUtilizado')
    op.drop_column('consultas', 'cupoAprobado')
    op.drop_column('consultas', 'antiguedad_cli')
    # ### end Alembic commands ###

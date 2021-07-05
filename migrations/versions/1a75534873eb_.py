"""empty message

Revision ID: 1a75534873eb
Revises: a8042174a278
Create Date: 2021-06-26 11:37:50.249388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a75534873eb'
down_revision = 'a8042174a278'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('consultas', sa.Column('trabajadoresSuspendidos', sa.Integer(), nullable=True))
    op.add_column('consultas', sa.Column('score_externo', sa.Integer(), nullable=True))
    op.add_column('consultas', sa.Column('score_rdf', sa.Integer(), nullable=True))
    op.drop_column('consultas', 'score')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('consultas', sa.Column('score', sa.FLOAT(), nullable=True))
    op.drop_column('consultas', 'score_rdf')
    op.drop_column('consultas', 'score_externo')
    op.drop_column('consultas', 'trabajadoresSuspendidos')
    # ### end Alembic commands ###

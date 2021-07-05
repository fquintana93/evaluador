"""empty message

Revision ID: fcc0af5183bc
Revises: 94c534ca552b
Create Date: 2021-06-26 10:55:49.237644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcc0af5183bc'
down_revision = '94c534ca552b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('consultas', sa.Column('correlativo', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_consultas_correlativo'), 'consultas', ['correlativo'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_consultas_correlativo'), table_name='consultas')
    op.drop_column('consultas', 'correlativo')
    # ### end Alembic commands ###
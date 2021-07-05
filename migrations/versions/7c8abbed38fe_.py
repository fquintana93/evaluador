"""empty message

Revision ID: 7c8abbed38fe
Revises: 1a75534873eb
Create Date: 2021-06-26 13:03:18.561379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c8abbed38fe'
down_revision = '1a75534873eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('consultas', sa.Column('correlativo', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('consultas', 'correlativo')
    # ### end Alembic commands ###

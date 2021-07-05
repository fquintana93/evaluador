"""empty message

Revision ID: 18d24830a583
Revises: 0153592255f6
Create Date: 2021-06-12 16:15:43.742124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18d24830a583'
down_revision = '0153592255f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('consultas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('score_final', sa.Integer(), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('score_final')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('score_final', sa.INTEGER(), nullable=True))

    with op.batch_alter_table('consultas', schema=None) as batch_op:
        batch_op.drop_column('score_final')

    # ### end Alembic commands ###
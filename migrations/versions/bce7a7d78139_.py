"""empty message

Revision ID: bce7a7d78139
Revises: 4ac2b3a5c48d
Create Date: 2021-06-10 20:55:55.426908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bce7a7d78139'
down_revision = '4ac2b3a5c48d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sii', schema=None) as batch_op:
        batch_op.alter_column('rut',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sii', schema=None) as batch_op:
        batch_op.alter_column('rut',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)

    # ### end Alembic commands ###

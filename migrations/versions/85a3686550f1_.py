"""empty message

Revision ID: 85a3686550f1
Revises: 16f4a169cd34
Create Date: 2021-06-10 12:27:27.976438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85a3686550f1'
down_revision = '16f4a169cd34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'consultas', 'admin', ['empresa_id'], ['id'])
    op.add_column('user', sa.Column('name', sa.String(length=64), nullable=True))
    op.add_column('user', sa.Column('lastname', sa.String(length=64), nullable=True))
    op.add_column('user', sa.Column('empresa_id', sa.Integer(), nullable=True))
    op.drop_index('ix_user_empresa', table_name='user')
    op.create_foreign_key(None, 'user', 'admin', ['empresa_id'], ['id'])
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'empresa')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('empresa', sa.VARCHAR(length=64), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DATETIME(), nullable=True))
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.create_index('ix_user_empresa', 'user', ['empresa'], unique=False)
    op.drop_column('user', 'empresa_id')
    op.drop_column('user', 'lastname')
    op.drop_column('user', 'name')
    op.drop_constraint(None, 'consultas', type_='foreignkey')
    # ### end Alembic commands ###

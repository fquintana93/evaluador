"""followers

Revision ID: 659c893d5dde
Revises: c8dc61a87fc2
Create Date: 2021-06-08 14:40:26.873393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '659c893d5dde'
down_revision = 'c8dc61a87fc2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###

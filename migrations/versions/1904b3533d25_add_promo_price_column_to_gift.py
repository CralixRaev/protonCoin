"""add promo price column to gift

Revision ID: 1904b3533d25
Revises: ee1e5ed4fc7c
Create Date: 2022-12-12 13:55:06.670525

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1904b3533d25'
down_revision = 'ee1e5ed4fc7c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('gift', schema=None) as batch_op:
        batch_op.add_column(sa.Column('promo_price', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
   with op.batch_alter_table('gift', schema=None) as batch_op:
        batch_op.drop_column('promo_price')
    # ### end Alembic commands ###

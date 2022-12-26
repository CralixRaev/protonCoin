"""create news table

Revision ID: ee1e5ed4fc7c
Revises: d3b23c646b74
Create Date: 2022-12-06 15:53:40.672373

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ee1e5ed4fc7c'
down_revision = 'd3b23c646b74'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_news'))
    )
    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_news_id'), ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_news_id'))

    op.drop_table('news')
    # ### end Alembic commands ###
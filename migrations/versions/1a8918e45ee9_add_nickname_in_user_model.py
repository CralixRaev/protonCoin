"""add nickname in user model

Revision ID: 1a8918e45ee9
Revises: 1904b3533d25
Create Date: 2023-01-18 20:02:34.700833

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Session

from db.models.user import User

# revision identifiers, used by Alembic.
revision = '1a8918e45ee9'
down_revision = '1904b3533d25'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    session = Session(bind=conn)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nickname', sa.String(length=16), nullable=True))
        batch_op.create_index(batch_op.f('ix_user_nickname'), ['nickname'], unique=True)

    session.commit()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_nickname'))
        batch_op.drop_column('nickname')

    # ### end Alembic commands ###

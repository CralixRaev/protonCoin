"""add alternative_id for invalidating user sessions when they change password and last user auth time

Revision ID: 2361538ac6c0
Revises: c08132e6a185
Create Date: 2022-11-12 00:07:53.073290

"""

from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from protonCoin.db.models.user import User

# revision identifiers, used by Alembic.
revision = "2361538ac6c0"
down_revision = "c08132e6a185"
branch_labels = None
depends_on = None

Base = automap_base()


def upgrade():
    conn = op.get_bind()
    session = Session(bind=conn)

    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("last_auth", sa.DateTime(), nullable=True))
        batch_op.add_column(
            sa.Column("alternative_id", sa.String(length=36), nullable=True)
        )

    for item in session.query(User).all():
        item.alternative_id = str(uuid4())
    session.commit()

    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column("alternative_id", nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("alternative_id")
        batch_op.drop_column("last_auth")

    # ### end Alembic commands ###
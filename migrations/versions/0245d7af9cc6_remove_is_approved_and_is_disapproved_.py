"""remove is_approved and is_disapproved and change it to one status enum

Revision ID: 0245d7af9cc6
Revises: 2361538ac6c0
Create Date: 2022-11-20 17:43:22.187940

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Session, declarative_base

from db.models.achievement import AchievementStatusEnum
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0245d7af9cc6'
down_revision = '2361538ac6c0'
branch_labels = None
depends_on = None

Base = declarative_base()


class Achievement(Base):
    __tablename__ = 'achievement'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    achievement_file = sa.Column(sa.String(1024), nullable=True)
    comment = sa.Column(sa.String(4096), nullable=True)
    creation_date = sa.Column(sa.DateTime, default=datetime.now)
    edit_date = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)
    status = sa.Column(sa.Enum(AchievementStatusEnum),
                       default=AchievementStatusEnum.awaiting_approval, nullable=False)
    is_approved = sa.Column(sa.Boolean, default=False, nullable=False)
    is_disapproved = sa.Column(sa.Boolean, default=False, nullable=False)
    disapproval_reason = sa.Column(sa.String(4096), nullable=True, default=None)


def upgrade():
    conn = op.get_bind()
    session = Session(bind=conn)
    achievementstatus_enum = postgresql.ENUM(*[i.value for i in AchievementStatusEnum],
                                             name='achievementstatus', create_type=False)
    achievementstatus_enum.create(op.get_bind(), checkfirst=True)
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('achievement', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', achievementstatus_enum, nullable=True))

    for item in session.query(Achievement).all():
        if item.is_approved:
            item.status = 'approved'
        elif item.is_disapproved:
            item.status = 'disapproved'
        else:
            item.status = 'awaiting_approval'
    session.commit()

    with op.batch_alter_table('achievement', schema=None) as batch_op:
        batch_op.drop_column('is_disapproved')
        batch_op.drop_column('is_approved')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('achievement', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('is_approved', sa.BOOLEAN(), autoincrement=False, nullable=False))
        batch_op.add_column(
            sa.Column('is_disapproved', sa.BOOLEAN(), autoincrement=False, nullable=False))
        batch_op.drop_column('status')

    # ### end Alembic commands ###
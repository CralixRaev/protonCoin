"""initial with gift table

Revision ID: c3d01a6e11ad
Revises: 
Create Date: 2022-05-09 09:11:54.699049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3d01a6e11ad'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gift',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_gift'))
    )
    with op.batch_alter_table('gift', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_gift_id'), ['id'], unique=False)

    op.create_table('group',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('stage', sa.Integer(), nullable=False),
    sa.Column('letter', sa.String(length=8), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_group'))
    )
    with op.batch_alter_table('group', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_group_id'), ['id'], unique=False)

    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('login', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('surname', sa.String(length=32), nullable=False),
    sa.Column('patronymic', sa.String(length=32), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], name=op.f('fk_user_group_id_group')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_group_id'), ['group_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_login'), ['login'], unique=True)

    op.create_table('balance',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_balance_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_balance'))
    )
    with op.batch_alter_table('balance', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_balance_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_balance_user_id'), ['user_id'], unique=True)

    op.create_table('transaction',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('from_balance_id', sa.Integer(), nullable=False),
    sa.Column('to_balance_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['from_balance_id'], ['balance.id'], name=op.f('fk_transaction_from_balance_id_balance')),
    sa.ForeignKeyConstraint(['to_balance_id'], ['balance.id'], name=op.f('fk_transaction_to_balance_id_balance')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_transaction'))
    )
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_transaction_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_transaction_id'))

    op.drop_table('transaction')
    with op.batch_alter_table('balance', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_balance_user_id'))
        batch_op.drop_index(batch_op.f('ix_balance_id'))

    op.drop_table('balance')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_login'))
        batch_op.drop_index(batch_op.f('ix_user_id'))
        batch_op.drop_index(batch_op.f('ix_user_group_id'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    with op.batch_alter_table('group', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_group_id'))

    op.drop_table('group')
    with op.batch_alter_table('gift', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_gift_id'))

    op.drop_table('gift')
    # ### end Alembic commands ###
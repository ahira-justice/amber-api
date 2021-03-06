"""Remove PasswordReset entity

Revision ID: d38580858ea5
Revises: c660e719ce1d
Create Date: 2022-01-26 11:28:13.227547

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd38580858ea5'
down_revision = 'c660e719ce1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_passwordresets_id', table_name='passwordresets')
    op.drop_index('ix_passwordresets_reset_code', table_name='passwordresets')
    op.drop_table('passwordresets')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('passwordresets',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('reset_code', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('expiry', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='passwordresets_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='passwordresets_pkey')
    )
    op.create_index('ix_passwordresets_reset_code', 'passwordresets', ['reset_code'], unique=False)
    op.create_index('ix_passwordresets_id', 'passwordresets', ['id'], unique=False)
    # ### end Alembic commands ###

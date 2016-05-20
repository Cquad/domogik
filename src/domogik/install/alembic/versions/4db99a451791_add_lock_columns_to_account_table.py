"""Add lock columns to account table

Revision ID: 4db99a451791
Revises: 2269ae8c2bc7
Create Date: 2016-05-20 20:35:52.911285

"""

# revision identifiers, used by Alembic.
revision = '4db99a451791'
down_revision = '2269ae8c2bc7'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('core_user_account', sa.Column('lock_delete', sa.Boolean(), nullable=False))
    op.add_column('core_user_account', sa.Column('lock_edit', sa.Boolean(), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('core_user_account', 'lock_edit')
    op.drop_column('core_user_account', 'lock_delete')
    ### end Alembic commands ###

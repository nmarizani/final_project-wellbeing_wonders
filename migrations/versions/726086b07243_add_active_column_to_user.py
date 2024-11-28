"""Add active column to User

Revision ID: 726086b07243
Revises: 58423cff756b
Create Date: 2024-11-28 14:29:23.587258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '726086b07243'
down_revision = '58423cff756b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('active', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('active')

    # ### end Alembic commands ###
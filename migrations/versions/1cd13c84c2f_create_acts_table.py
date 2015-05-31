"""create acts table

Revision ID: 1cd13c84c2f
Revises: 
Create Date: 2015-05-31 14:14:29.331906

"""

# revision identifiers, used by Alembic.
revision = '1cd13c84c2f'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'acts',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('code', sa.String(50)),
        sa.Column('short_title', sa.String(65000)),
        sa.Column('long_title', sa.String(65000)),
        sa.Column('act_date', sa.String(10)),
        sa.Column('language', sa.String(10))
    )


def downgrade():
    op.drop_table('acts')

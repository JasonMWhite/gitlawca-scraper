"""add law URL

Revision ID: 3a652126bcd5
Revises: 1cd13c84c2f
Create Date: 2015-06-01 00:10:55.672883

"""

# revision identifiers, used by Alembic.
revision = '3a652126bcd5'
down_revision = '1cd13c84c2f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('acts', sa.Column('url', sa.String(1000)))


def downgrade():
    op.drop_column('acts', 'url')

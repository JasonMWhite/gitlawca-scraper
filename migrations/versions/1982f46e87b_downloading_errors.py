"""downloading errors

Revision ID: 1982f46e87b
Revises: 3a652126bcd5
Create Date: 2015-06-04 08:26:46.521281

"""

# revision identifiers, used by Alembic.
revision = '1982f46e87b'
down_revision = '3a652126bcd5'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('acts', sa.Column('error_downloading', sa.Boolean, default=False))


def downgrade():
    op.drop_column('acts', 'error_downloading')

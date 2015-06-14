"""add_git_commit

Revision ID: 2dbb6292b4f
Revises: 1982f46e87b
Create Date: 2015-06-14 16:11:16.081725

"""

# revision identifiers, used by Alembic.
revision = '2dbb6292b4f'
down_revision = '1982f46e87b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('acts', sa.Column('git_commit', sa.String(40)))


def downgrade():
    op.drop_column('acts', 'git_commit')

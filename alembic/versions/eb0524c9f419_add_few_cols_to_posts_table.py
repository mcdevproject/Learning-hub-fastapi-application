"""add few cols to posts table

Revision ID: eb0524c9f419
Revises: c8557cebb225
Create Date: 2022-02-24 13:13:55.482083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb0524c9f419'
down_revision = 'c8557cebb225'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(),
                  nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default='NOW()'))


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')

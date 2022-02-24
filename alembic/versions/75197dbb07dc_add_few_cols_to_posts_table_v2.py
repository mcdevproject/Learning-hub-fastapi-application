"""add few cols to posts table v2

Revision ID: 75197dbb07dc
Revises: eb0524c9f419
Create Date: 2022-02-24 13:21:49.251467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75197dbb07dc'
down_revision = 'eb0524c9f419'
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

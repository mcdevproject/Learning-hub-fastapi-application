"""add content column to posts table

Revision ID: 9f3c0ce4ec3d
Revises: 27f10b50ffe0
Create Date: 2022-02-24 11:38:35.628244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f3c0ce4ec3d'
down_revision = '27f10b50ffe0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')

"""remove phone_number in user table

Revision ID: de62ed01152a
Revises: 71c8e245a631
Create Date: 2022-02-26 02:43:55.816647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de62ed01152a'
down_revision = '71c8e245a631'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('users', 'phone_number')


def downgrade():
    op.add_column('users', sa.Column(
        'phone_number', sa.String, nullable=False))

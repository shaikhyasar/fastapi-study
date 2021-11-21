"""create posts table

Revision ID: b2d33cc87458
Revises: 2244c7e99df7
Create Date: 2021-11-21 03:20:21.872706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2d33cc87458'
down_revision = '2244c7e99df7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id',sa.Integer,nullable=False),
                    sa.Column('title',sa.String,nullable=False)
    )
    pass


def downgrade():
    op.drop_table('posts')
    pass

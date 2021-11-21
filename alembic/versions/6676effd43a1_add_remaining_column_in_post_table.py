"""add remaining column in post table

Revision ID: 6676effd43a1
Revises: b946bb42e142
Create Date: 2021-11-21 17:18:40.099940

"""
from enum import Flag
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6676effd43a1'
down_revision = 'b946bb42e142'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String,nullable=False))
    op.add_column('posts',sa.Column('published',sa.Boolean,nullable=True,server_default="TRUE"))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                    nullable=False,server_default=sa.text('now()'),))
    pass


def downgrade():
    op.drop_Column('posts','content')
    op.drop_Column('posts','published')
    op.drop_Column('posts','created_at')
    pass

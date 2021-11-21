"""create user table

Revision ID: 2244c7e99df7
Revises: 3e0f62223b8c
Create Date: 2021-11-21 02:00:10.625869

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2244c7e99df7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
            sa.Column('id',sa.Integer,nullable=False),
            sa.Column('name',sa.String,nullable=False),
            sa.Column('email',sa.String,nullable=False),
            sa.Column('password',sa.String,nullable=False),
            sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()'),),
            sa.UniqueConstraint('email'),
            sa.PrimaryKeyConstraint('id')
            )


def downgrade():
    op.drop_table('users')

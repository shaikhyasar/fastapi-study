"""create foreign key to post table

Revision ID: b946bb42e142
Revises: b2d33cc87458
Create Date: 2021-11-21 16:38:07.004779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b946bb42e142'
down_revision = 'b2d33cc87458'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                    sa.Column('owner_id',sa.Integer,nullable=False))
    op.create_foreign_key('posts_users_fk',source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass

"""removed title field

Revision ID: 2a9fa4513d6d
Revises: ba5e60aaab49
Create Date: 2022-07-24 05:21:02.476165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a9fa4513d6d'
down_revision = 'ba5e60aaab49'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('videos', 'title')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('videos', sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

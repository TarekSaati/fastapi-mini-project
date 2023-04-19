"""creating posts table

Revision ID: 1d26fcfbb057
Revises: 
Create Date: 2023-04-17 12:13:46.221545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d26fcfbb057'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',  
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean(), nullable=False, default=True)
                    )


def downgrade() -> None:
    op.drop_table('posts')

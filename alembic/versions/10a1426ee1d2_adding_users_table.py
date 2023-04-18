"""adding users table

Revision ID: 10a1426ee1d2
Revises: 1d26fcfbb057
Create Date: 2023-04-17 12:31:12.295775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10a1426ee1d2'
down_revision = '1d26fcfbb057'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',  
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('firstName', sa.String(), nullable=False),
                    sa.Column('lastName', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade() -> None:
    op.drop_table('users')

"""initial

Revision ID: c5027c6a3847
Revises: 
Create Date: 2025-05-16 09:35:10.110052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5027c6a3847'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file_info',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('uri', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tokens',
    sa.Column('access_token', sa.String(length=255), nullable=False),
    sa.Column('token_type', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('access_token'),
    sa.UniqueConstraint('access_token')
    )
    op.create_table('users',
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('username'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('tokens')
    op.drop_table('file_info')
    # ### end Alembic commands ###

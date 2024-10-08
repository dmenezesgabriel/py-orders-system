"""feat: add order estimated_time

Revision ID: bd731bd95d00
Revises: e916d69bbc44
Create Date: 2024-08-25 21:53:58.737928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd731bd95d00'
down_revision: Union[str, None] = 'e916d69bbc44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('estimated_time', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'estimated_time')
    # ### end Alembic commands ###

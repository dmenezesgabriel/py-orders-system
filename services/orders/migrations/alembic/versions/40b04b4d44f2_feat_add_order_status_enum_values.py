"""feat: add order status enum values

Revision ID: 40b04b4d44f2
Revises: bd731bd95d00
Create Date: 2024-08-25 22:10:37.271713

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "40b04b4d44f2"
down_revision: Union[str, None] = "bd731bd95d00"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TYPE orderstatus ADD VALUE 'RECEIVED'")
    op.execute("ALTER TYPE orderstatus ADD VALUE 'PREPARING'")
    op.execute("ALTER TYPE orderstatus ADD VALUE 'READY'")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

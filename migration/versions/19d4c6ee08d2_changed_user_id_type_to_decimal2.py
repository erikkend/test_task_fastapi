"""changed user_id type to decimal2

Revision ID: 19d4c6ee08d2
Revises: 121f18e7c939
Create Date: 2025-01-22 21:39:47.283508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19d4c6ee08d2'
down_revision: Union[str, None] = '121f18e7c939'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'user_id',
               existing_type=sa.BIGINT(),
               type_=sa.DECIMAL(precision=21, scale=2),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'user_id',
               existing_type=sa.DECIMAL(precision=21, scale=2),
               type_=sa.BIGINT(),
               existing_nullable=False)
    # ### end Alembic commands ###

"""changed user_id type to bigint

Revision ID: 121f18e7c939
Revises: c1628a0bd5e8
Create Date: 2025-01-21 23:32:50.869118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '121f18e7c939'
down_revision: Union[str, None] = 'c1628a0bd5e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'user_id',
               existing_type=sa.NUMERIC(precision=21, scale=0),
               type_=sa.BigInteger(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'user_id',
               existing_type=sa.BigInteger(),
               type_=sa.NUMERIC(precision=21, scale=0),
               existing_nullable=False)
    # ### end Alembic commands ###

"""changed user_id type

Revision ID: c1628a0bd5e8
Revises: 9a3c6697c5f6
Create Date: 2025-01-21 20:46:10.187727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1628a0bd5e8'
down_revision: Union[str, None] = '9a3c6697c5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'user_id',
               existing_type=sa.INTEGER(),
               type_=sa.Numeric(precision=21, scale=0),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'user_id',
               existing_type=sa.Numeric(precision=21, scale=0),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###

"""Add order_index to Award and Conference for manual display ordering

기존 행은 order_index = id 로 backfill 한다 (공개 페이지의 완전 수동 정렬용,
내림차순 정렬이므로 기본값 기준으로는 최신 항목이 위에 온다).

Revision ID: f8a9b0c1d2e3
Revises: e6f7a8b9c0d1
Create Date: 2026-07-15 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'f8a9b0c1d2e3'
down_revision: Union[str, Sequence[str], None] = 'e6f7a8b9c0d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('award', sa.Column('order_index', sa.Integer(), nullable=True))
    op.add_column('conference', sa.Column('order_index', sa.Integer(), nullable=True))
    op.execute('UPDATE award SET order_index = id WHERE order_index IS NULL')
    op.execute('UPDATE conference SET order_index = id WHERE order_index IS NULL')


def downgrade() -> None:
    op.drop_column('conference', 'order_index')
    op.drop_column('award', 'order_index')

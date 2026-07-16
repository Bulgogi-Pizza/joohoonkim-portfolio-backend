"""Renumber order_index for ascending manual ordering (1 = top)

정렬 방향이 내림차순 → 오름차순으로 바뀜에 따라, 기존 표시 순서(최신이 위)를
그대로 유지하도록 order_index를 1..N으로 재부여한다:
- award: 연도(문자열 앞 4자리) 내림차순, 동률은 id 내림차순 → 1..N
- conference: date 내림차순, 동률은 id 내림차순 → 1..N

Revision ID: a7b8c9d0e1f2
Revises: f8a9b0c1d2e3
Create Date: 2026-07-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

revision: str = 'a7b8c9d0e1f2'
down_revision: Union[str, Sequence[str], None] = 'f8a9b0c1d2e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        WITH ranked AS (
            SELECT id, ROW_NUMBER() OVER (
                ORDER BY CAST(SUBSTR(year, 1, 4) AS INTEGER) DESC, id DESC
            ) AS rn
            FROM award
        )
        UPDATE award SET order_index = (SELECT rn FROM ranked WHERE ranked.id = award.id)
    """)
    op.execute("""
        WITH ranked AS (
            SELECT id, ROW_NUMBER() OVER (
                ORDER BY date DESC, id DESC
            ) AS rn
            FROM conference
        )
        UPDATE conference SET order_index = (SELECT rn FROM ranked WHERE ranked.id = conference.id)
    """)


def downgrade() -> None:
    # 이전 기본값(order_index = id)으로 되돌린다
    op.execute('UPDATE award SET order_index = id')
    op.execute('UPDATE conference SET order_index = id')

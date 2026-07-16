"""Renumber order_index for descending manual ordering (largest = top)

정렬 방향이 다시 내림차순으로 확정됨에 따라, 최신 항목이 가장 큰 값을 갖도록
order_index를 재부여한다 (오래된 것 = 1, 최신 = N):
- award: 연도(문자열 앞 4자리) 오름차순, 동률은 id 오름차순 → 1..N
- conference: date 오름차순, 동률은 id 오름차순 → 1..N

새 항목은 생성 시 order_index = id(항상 기존 최대값보다 큼)라서 자동으로 맨 위에 온다.

Revision ID: c3d4e5f6a7b8
Revises: a7b8c9d0e1f2
Create Date: 2026-07-16 00:30:00.000000

"""
from typing import Sequence, Union

from alembic import op

revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, Sequence[str], None] = 'a7b8c9d0e1f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        WITH ranked AS (
            SELECT id, ROW_NUMBER() OVER (
                ORDER BY CAST(SUBSTR(year, 1, 4) AS INTEGER) ASC, id ASC
            ) AS rn
            FROM award
        )
        UPDATE award SET order_index = (SELECT rn FROM ranked WHERE ranked.id = award.id)
    """)
    op.execute("""
        WITH ranked AS (
            SELECT id, ROW_NUMBER() OVER (
                ORDER BY date ASC, id ASC
            ) AS rn
            FROM conference
        )
        UPDATE conference SET order_index = (SELECT rn FROM ranked WHERE ranked.id = conference.id)
    """)


def downgrade() -> None:
    # 직전(오름차순 기준) 재부여로 되돌린다: 최신 = 1
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

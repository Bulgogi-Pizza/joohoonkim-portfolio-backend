"""Add award category, member table and opening table

- award.category: 기존 행은 모두 PI 수상으로 간주한다 (server_default 'pi')
- member: 연구실 구성원 (pi / researcher / alumni)
- opening: 모집 공고 마크다운 단일 문서, 빈 내용으로 한 행을 시드한다

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-10-11 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, Sequence[str], None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'award',
        sa.Column('category', sqlmodel.sql.sqltypes.AutoString(), nullable=False, server_default='pi'),
    )
    op.create_table(
        'member',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('category', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('position', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('research_interest', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('education', sa.JSON(), nullable=False),
        sa.Column('image_path', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('order_index', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'opening',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.execute("INSERT INTO opening (content, updated_at) VALUES ('', timezone('utc', now()))")


def downgrade() -> None:
    op.drop_table('opening')
    op.drop_table('member')
    op.drop_column('award', 'category')

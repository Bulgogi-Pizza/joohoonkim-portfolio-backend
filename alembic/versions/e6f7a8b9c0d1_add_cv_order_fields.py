"""Add cv_order field to Education, Experience, Award, Publication, CVService

Revision ID: e6f7a8b9c0d1
Revises: d5e6f7a8b9c0
Create Date: 2026-04-18 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'e6f7a8b9c0d1'
down_revision: Union[str, Sequence[str], None] = 'd5e6f7a8b9c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('education', sa.Column('cv_order', sa.Integer(), nullable=True))
    op.add_column('experience', sa.Column('cv_order', sa.Integer(), nullable=True))
    op.add_column('award', sa.Column('cv_order', sa.Integer(), nullable=True))
    op.add_column('publication', sa.Column('cv_order', sa.Integer(), nullable=True))
    op.add_column('cvservice', sa.Column('cv_order', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('cvservice', 'cv_order')
    op.drop_column('publication', 'cv_order')
    op.drop_column('award', 'cv_order')
    op.drop_column('experience', 'cv_order')
    op.drop_column('education', 'cv_order')

"""Seed initial CVService data

Revision ID: d5e6f7a8b9c0
Revises: c4d5e6f7a8b9
Create Date: 2026-04-18 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'd5e6f7a8b9c0'
down_revision: Union[str, Sequence[str], None] = 'c4d5e6f7a8b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

CV_SERVICES = [
    {
        "title": "Proposal Reviewer",
        "description": "Served as proposal reviewer for Israeli Ministry of Innovation, Science and Technology",
        "order_index": 1,
    },
    {
        "title": "Journal Reviewer",
        "description": (
            "Regular reviewer for Nature Communications, Light: Science & Applications, "
            "Microsystems & Nanoengineering, Laser & Photonics Reviews, ACS Photonics, Optica, "
            "Nanophotonics, Communications Physics, npj Nanophotonics, Scientific Reports, "
            "Optics Express, Optics Letters, Optics and Laser Technology, Nanomaterials, Displays."
        ),
        "order_index": 2,
    },
]


def upgrade() -> None:
    for service in CV_SERVICES:
        op.execute(
            sa.text(
                "INSERT INTO cvservice (title, description, order_index, created_at, updated_at) "
                "VALUES (:title, :description, :order_index, NOW(), NOW())"
            ).bindparams(**service)
        )


def downgrade() -> None:
    op.execute("DELETE FROM cvservice WHERE title IN ('Proposal Reviewer', 'Journal Reviewer')")

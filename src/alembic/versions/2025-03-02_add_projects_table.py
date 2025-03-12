"""add projects table

Revision ID: 5eb77e0283a8
Revises: 69fe0474678c
Create Date: 2025-03-02 14:05:17.767123

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op  # type: ignore

# revision identifiers, used by Alembic.
revision: str = "5eb77e0283a8"
down_revision: Union[str, None] = "69fe0474678c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("name", sa.String(length=40), nullable=False),
        sa.Column("description", sa.String(length=150), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("owner_id", sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_foreign_key("fk_projects_owner_id_users", "projects", "users", ["owner_id"], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("fk_projects_owner_id_users", "projects", type_="foreignkey")
    op.drop_table("projects")

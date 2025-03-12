"""add permissions table

Revision ID: 69cd1fd46e2a
Revises: 05032a1505f1
Create Date: 2025-03-02 16:11:35.439730

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op  # type: ignore

# revision identifiers, used by Alembic.
revision: str = "69cd1fd46e2a"
down_revision: Union[str, None] = "05032a1505f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "permissions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_role", sa.Enum("OWNER", "PARTICIPANT", "VIEWER", name="user_role"), nullable=False),
        sa.Column(
            "request_status",
            sa.Enum("PENDING", "ACCEPTED", "REJECTED", name="request_status"),
            nullable=False,
            server_default="PENDING",
        ),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("project_id", sa.Integer, sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.UniqueConstraint("user_id", "project_id", name="uq_user_project"),
    )


def downgrade() -> None:
    op.drop_table("permissions")

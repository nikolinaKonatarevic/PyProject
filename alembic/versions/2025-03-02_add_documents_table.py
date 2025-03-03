"""add documents table

Revision ID: 05032a1505f1
Revises: 5eb77e0283a8
Create Date: 2025-03-02 14:07:31.375987

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op  # type: ignore

# revision identifiers, used by Alembic.
revision: str = "05032a1505f1"
down_revision: Union[str, None] = "5eb77e0283a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("file_name", sa.String(25), nullable=False),
        sa.Column("file_path", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column("project_id", sa.Integer, nullable=False),
    )
    op.create_foreign_key(
        "fk_documents_project_id_projects", "documents", "projects", ["project_id"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint("fk_documents_project_id_projects", "documents", type_="foreignkey")
    op.drop_table("documents")

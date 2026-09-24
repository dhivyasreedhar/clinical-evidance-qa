"""immutable independently cached source extractions"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "e42a135c902d"
down_revision = "c910a83d291a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "source_extractions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("patient_id", sa.Uuid(), nullable=False),
        sa.Column("revision_id", sa.Uuid(), nullable=False),
        sa.Column("cache_key", sa.String(64), nullable=False),
        sa.Column("data", postgresql.JSONB(), nullable=False),
        sa.Column("usage", postgresql.JSONB(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.UniqueConstraint("tenant_id", "patient_id", "revision_id", "cache_key"),
        sa.ForeignKeyConstraint(
            ["tenant_id", "patient_id", "revision_id"],
            [
                "document_revisions.tenant_id",
                "document_revisions.patient_id",
                "document_revisions.id",
            ],
        ),
    )
    op.create_index("ix_source_extractions_tenant_id", "source_extractions", ["tenant_id"])
    op.execute("ALTER TABLE source_extractions ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE source_extractions FORCE ROW LEVEL SECURITY")
    op.execute(
        "CREATE POLICY tenant_isolation ON source_extractions USING (tenant_id = current_setting('app.tenant_id', true)::uuid) WITH CHECK (tenant_id = current_setting('app.tenant_id', true)::uuid)"
    )
    op.execute("GRANT SELECT, INSERT ON source_extractions TO ehr_app")


def downgrade() -> None:
    op.drop_table("source_extractions")

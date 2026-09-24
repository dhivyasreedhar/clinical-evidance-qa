"""append-only document withdrawal and restoration events"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision = "f3a1c9d2b7e4"
down_revision = "e42a135c902d"
branch_labels = None
depends_on = None


def manifest_constraint() -> str | None:
    for constraint in inspect(op.get_bind()).get_unique_constraints("snapshots"):
        if constraint["column_names"] == ["tenant_id", "patient_id", "manifest_hash"]:
            return str(constraint["name"])
    return None


def upgrade() -> None:
    op.create_table(
        "document_status_events",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("patient_id", sa.Uuid(), nullable=False),
        sa.Column("revision_id", sa.Uuid(), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=False),
        sa.Column("action", sa.String(20), nullable=False),
        sa.Column("reason", sa.String(500), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "patient_id", "revision_id"],
            [
                "document_revisions.tenant_id",
                "document_revisions.patient_id",
                "document_revisions.id",
            ],
        ),
        sa.CheckConstraint("action IN ('withdrawn','restored')", name="document_status_action"),
    )
    op.create_index(
        "ix_document_status_events_revision",
        "document_status_events",
        ["tenant_id", "revision_id", "created_at"],
    )
    op.execute("ALTER TABLE document_status_events ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE document_status_events FORCE ROW LEVEL SECURITY")
    op.execute(
        "CREATE POLICY tenant_scope ON document_status_events USING (tenant_id = NULLIF(current_setting('app.tenant_id', true), '')::uuid) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id', true), '')::uuid)"
    )
    # Append-only: the app may record events but never rewrite them.
    op.execute("GRANT SELECT, INSERT ON document_status_events TO ehr_app")
    # Withdrawing then restoring returns to an earlier manifest; that is a new snapshot, not a
    # conflict. Snapshots are still unique by sequence.
    name = manifest_constraint()
    if name:
        op.drop_constraint(name, "snapshots", type_="unique")


def downgrade() -> None:
    op.drop_table("document_status_events")
    op.create_unique_constraint(
        "snapshots_tenant_id_patient_id_manifest_hash_key",
        "snapshots",
        ["tenant_id", "patient_id", "manifest_hash"],
    )

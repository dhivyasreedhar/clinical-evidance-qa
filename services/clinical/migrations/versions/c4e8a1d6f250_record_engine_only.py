"""record engine only: drop the evidence pipeline's tasks, results and extraction cache"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect
from sqlalchemy.dialects import postgresql

revision = "c4e8a1d6f250"
down_revision = "a7d2e5f81c30"
branch_labels = None
depends_on = None

ENGINE = "'engine_record','engine_answer'"


def replace_constraints(kinds: str, standalone: str, answers: str) -> None:
    for constraint in inspect(op.get_bind()).get_check_constraints("analysis_tasks"):
        if "kind" in constraint["sqltext"] and constraint["name"]:
            op.drop_constraint(constraint["name"], "analysis_tasks", type_="check")
    op.create_check_constraint("analysis_kind", "analysis_tasks", f"kind IN ({kinds})")
    op.create_check_constraint(
        "analysis_kind_payload",
        "analysis_tasks",
        f"(kind IN ({standalone}) AND abstraction_id IS NULL AND question IS NULL) OR "
        f"(kind IN ({answers}) AND abstraction_id IS NOT NULL AND question IS NOT NULL)",
    )


def upgrade() -> None:
    op.execute(
        "DELETE FROM analysis_results WHERE task_id IN "
        f"(SELECT id FROM analysis_tasks WHERE kind NOT IN ({ENGINE}))"
    )
    op.execute(f"DELETE FROM analysis_tasks WHERE kind NOT IN ({ENGINE})")
    op.drop_table("source_extractions")
    replace_constraints(ENGINE, "'engine_record'", "'engine_answer'")


def downgrade() -> None:
    # The deleted pipeline results are not restored; the empty cache table and wider checks are.
    replace_constraints(
        "'abstraction','answer','documents','engine_record','engine_answer'",
        "'abstraction','documents','engine_record'",
        "'answer','engine_answer'",
    )
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

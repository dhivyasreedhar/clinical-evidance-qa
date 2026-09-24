"""independent snapshot-pinned document catalog jobs"""

from alembic import op
from sqlalchemy import inspect

revision = "c910a83d291a"
down_revision = "ba5d37137dd2"
branch_labels = None
depends_on = None


def replace_constraints(include_documents: bool) -> None:
    # The initial migration used database-generated names for these checks.
    for constraint in inspect(op.get_bind()).get_check_constraints("analysis_tasks"):
        if "kind" in constraint["sqltext"] and constraint["name"]:
            op.drop_constraint(constraint["name"], "analysis_tasks", type_="check")
    kinds = "'abstraction','answer','documents'" if include_documents else "'abstraction','answer'"
    standalone = "'abstraction','documents'" if include_documents else "'abstraction'"
    op.create_check_constraint("analysis_kind", "analysis_tasks", f"kind IN ({kinds})")
    op.create_check_constraint(
        "analysis_kind_payload",
        "analysis_tasks",
        f"(kind IN ({standalone}) AND abstraction_id IS NULL AND question IS NULL) OR "
        "(kind = 'answer' AND abstraction_id IS NOT NULL AND question IS NOT NULL)",
    )


def upgrade() -> None:
    replace_constraints(True)


def downgrade() -> None:
    # Existing document jobs must be retained; the check prevents a destructive downgrade.
    replace_constraints(False)

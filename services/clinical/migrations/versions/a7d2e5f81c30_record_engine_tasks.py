"""record engine task kinds on the analysis queue"""

from alembic import op
from sqlalchemy import inspect

revision = "a7d2e5f81c30"
down_revision = "f3a1c9d2b7e4"
branch_labels = None
depends_on = None


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
    replace_constraints(
        "'abstraction','answer','documents','engine_record','engine_answer'",
        "'abstraction','documents','engine_record'",
        "'answer','engine_answer'",
    )


def downgrade() -> None:
    # Existing engine tasks must be retained; the check prevents a destructive downgrade.
    replace_constraints(
        "'abstraction','answer','documents'", "'abstraction','documents'", "'answer'"
    )

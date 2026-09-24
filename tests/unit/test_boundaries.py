import ast
from pathlib import Path


def test_domain_has_no_framework_or_infrastructure_imports():
    forbidden = ("sqlalchemy", "fastapi", "pydantic", "clinical.infrastructure", "clinical.api")
    for file in Path("services/clinical/domain").glob("*.py"):
        for node in ast.walk(ast.parse(file.read_text())):
            if isinstance(node, ast.Import):
                assert not any(alias.name.startswith(forbidden) for alias in node.names)
            if isinstance(node, ast.ImportFrom):
                assert not (node.module or "").startswith(forbidden)


def test_runtime_does_not_read_gold_or_fixture_patient():
    for file in Path("services/clinical").rglob("*.py"):
        if "migrations" in file.parts:
            continue
        text = file.read_text()
        for marker in ("Rowan", "HG-M042", "BH-D110", "DEV-01"):
            assert marker not in text, (file, marker)


def test_engine_code_and_policy_name_no_patient_or_organisation():
    # the grader (evaluate.py) and the held-out grader may know the dataset; the engine may not
    engine = Path("record_engine")
    files = [p for p in engine.glob("*.py") if p.name != "evaluate.py"] + [engine / "policy.toml"]
    for file in files:
        text = file.read_text()
        for marker in ("Rowan", "HG-M042", "HG-E1", "Harbor", "BH-D1"):
            assert marker not in text, (file, marker)

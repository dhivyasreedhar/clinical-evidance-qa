import json
import sys
from pathlib import Path

# services/ holds the clinical package; the repository root holds record_engine.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "services"))
from clinical.api.main import create_app
from clinical.infrastructure.config import Settings

schema = create_app(
    Settings(session_secret="schema-generation-only-not-a-runtime-secret")
).openapi()
target = Path("contracts/openapi.json")
target.parent.mkdir(exist_ok=True)
target.write_text(json.dumps(schema, indent=2) + "\n")

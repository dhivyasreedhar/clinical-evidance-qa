"""Generate the local session secret once without printing it."""

import secrets
from pathlib import Path

path = Path(".env")
if path.exists():
    print("Keeping existing .env")
else:
    template = Path(".env.example").read_text()
    template = template.replace(
        "replace-with-at-least-32-random-characters", secrets.token_urlsafe(48)
    )
    path.write_text(template)
    path.chmod(0o600)
    print("Created development .env")

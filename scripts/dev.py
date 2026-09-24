"""Run web/API/source worker together; stop only child processes we started."""

import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
browser_test = "--browser-test" in sys.argv
logs = ROOT / ".local" / ("browser-test-logs" if browser_test else "logs")
logs.mkdir(parents=True, exist_ok=True)
# services/ holds the clinical package; the repository root holds record_engine.
environment = dict(os.environ, PYTHONPATH=os.pathsep.join([str(ROOT / "services"), str(ROOT)]))
api_port = "8009" if browser_test else "8008"
web_port = "3001" if browser_test else "3000"
if browser_test:
    # Isolate fixtures at the database, identity, object-store and build-cache levels.
    # Explicit values override .env so tests cannot accidentally use the live workspace.
    run_id = str(uuid4())
    environment.update(
        {
            "EHR_ENVIRONMENT": "test",
            "EHR_DATABASE_URL": "postgresql+psycopg://ehr_app:local-development@127.0.0.1:55432/ehr_test",
            "EHR_DEV_TENANT": run_id,
            "EHR_DEV_ACTOR": str(uuid4()),
            "EHR_OBJECT_ROOT": str(ROOT / ".local" / "browser-test-objects" / run_id),
            "EHR_BROWSER_ORIGIN": "http://localhost:3001",
            "EHR_BROWSER_TEST": "1",
            "EHR_ANTHROPIC_API_KEY": "",
        }
    )
commands = {
    "api": [
        str(ROOT / ".venv/bin/uvicorn"),
        "clinical.api.main:create_app",
        "--factory",
        "--host",
        "127.0.0.1",
        "--port",
        api_port,
        "--no-access-log",
    ],
    "worker": [str(ROOT / ".venv/bin/python"), "-m", "clinical.workers.main"],
    "web": ["npm", "run", "dev", "--workspace", "apps/web", "--", "--port", web_port],
}
children: list[subprocess.Popen] = []
streams = []
running = True


def stop(*_: object) -> None:
    global running
    running = False


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)
try:
    for name, command in commands.items():
        stream = (logs / f"{name}.log").open("a")
        streams.append(stream)
        children.append(
            subprocess.Popen(
                command,
                env=environment,
                stdout=stream,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
        )
    print(f"Clinical Evidence: http://localhost:{web_port}", flush=True)
    print(
        f"API: http://127.0.0.1:{api_port}/docs · logs: {logs.relative_to(ROOT)} · Ctrl-C to stop",
        flush=True,
    )
    while running:
        if any(child.poll() is not None for child in children):
            print(
                f"A service stopped. Inspect {logs.relative_to(ROOT)} for the service status.",
                file=sys.stderr,
            )
            sys.exit(1)
        time.sleep(0.5)
finally:
    for child in children:
        if child.poll() is None:
            os.killpg(child.pid, signal.SIGTERM)
    for child in children:
        try:
            child.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.wait()
    for stream in streams:
        stream.close()

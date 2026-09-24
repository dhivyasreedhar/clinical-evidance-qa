.PHONY: setup db migrate dev check test integration contracts browser evaluate heldout scenarios

setup:
	python3 scripts/configure_local.py
	UV_CACHE_DIR=.cache/uv uv sync --frozen --python 3.13
	npm ci --cache .cache/npm

db:
	docker compose -f infra/compose.yaml up -d --wait

migrate:
	.venv/bin/alembic upgrade head
	EHR_MIGRATION_DATABASE_URL=postgresql+psycopg://ehr_owner:local-owner@127.0.0.1:55432/ehr_test .venv/bin/alembic upgrade head

dev:
	.venv/bin/python scripts/dev.py

contracts:
	.venv/bin/python scripts/export_openapi.py
	npm run contracts

check:
	.venv/bin/ruff check services record_engine tests scripts
	.venv/bin/ruff format --check services record_engine tests scripts
	.venv/bin/mypy
	npm run typecheck
	npx prettier --check apps/web/app apps/web/lib/api.ts apps/web/next.config.ts tests/browser playwright.config.ts

test:
	.venv/bin/pytest tests/unit record_engine/tests -q

integration:
	EHR_TEST_DATABASE_URL=postgresql+psycopg://ehr_app:local-development@127.0.0.1:55432/ehr_test .venv/bin/pytest tests/integration -q

browser:
	PLAYWRIGHT_BROWSERS_PATH=.cache/playwright npm run test:browser

# End-to-end run on documents/ + clinical_qa_benchmark/questions.json (paid model calls; model
# outputs are cached, so a re-run pays only for what changed). Writes the reviewable outputs to
# submission/: observations, the reconciled record and abstraction, the 65 answers, run costs,
# the judged and deterministic benchmark metrics, and a stability check (a second build from
# nothing, compared fact by fact). Needs EHR_ANTHROPIC_API_KEY in .env.
evaluate:
	.venv/bin/python -m record_engine observe --out submission
	.venv/bin/python -m record_engine build --out submission
	.venv/bin/python -m record_engine ask --questions clinical_qa_benchmark/questions.json \
		--gate DEV-01..05 --out submission
	.venv/bin/python -m record_engine.evaluate grade --answers submission/answers.json \
		--record submission/abstraction.json --out submission/benchmark/grades.json
	.venv/bin/python -m record_engine.evaluate score --answers submission/answers.json \
		--record submission/abstraction.json --grades submission/benchmark/grades.json \
		--out submission/benchmark/metrics.json
	.venv/bin/python -m record_engine.evaluate stability --record submission/abstraction.json \
		--out submission/benchmark/stability.json

# Held-out questions (reported separately; references are read only by the grader).
heldout:
	mkdir -p .local/re_heldout && cp submission/abstraction.json .local/re_heldout/
	.venv/bin/python -m record_engine ask --questions record_engine/heldout/questions.json \
		--out .local/re_heldout
	.venv/bin/python -m record_engine.heldout.grade --answers .local/re_heldout/answers.json \
		--out submission/benchmark/heldout_grades.json
	cp .local/re_heldout/answers.json submission/benchmark/heldout_answers.json

# Changed-input scenarios with the judge (see record_engine/scenarios/README.md).
scenarios:
	.venv/bin/python -m record_engine.scenarios.run --judge

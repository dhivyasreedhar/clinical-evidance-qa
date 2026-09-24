import logging
import signal
import time
from concurrent.futures import Future, ThreadPoolExecutor

from clinical.application.engine_runs import (
    RunLease,
    claim_run,
    enqueue_latest_records,
    process_run,
    release_run,
)
from clinical.application.imports import claim_job, process_job
from clinical.infrastructure.config import Settings
from clinical.infrastructure.database import make_engine
from clinical.infrastructure.objects import LocalObjectStore


def main() -> None:
    settings = Settings()
    engine = make_engine(settings.database_url)
    store = LocalObjectStore(settings.object_root)
    running = True
    # Different patients' runs execute concurrently (one per patient is enforced at enqueue),
    # so a short question is not queued behind another patient's multi-minute record build.
    executor = ThreadPoolExecutor(max_workers=settings.run_concurrency, thread_name_prefix="run")
    active: dict[Future[None], RunLease] = {}

    def stop(*_: object) -> None:
        nonlocal running
        running = False

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    try:
        while running:
            try:
                lease = claim_job(engine, settings.dev_tenant)
                if lease:
                    process_job(engine, store, settings.dev_tenant, lease, settings.max_file_bytes)
                for finished in [f for f in active if f.done()]:
                    del active[finished]
                    finished.result()
                if len(active) < settings.run_concurrency:
                    try:
                        enqueue_latest_records(engine, settings, settings.dev_tenant)
                    except Exception:
                        # an automatic rebuild that cannot be queued must not stop queued runs
                        logging.error("worker_enqueue_failed")
                while len(active) < settings.run_concurrency:
                    run = claim_run(engine, settings.dev_tenant, settings.run_lease_seconds)
                    if not run:
                        break
                    future = executor.submit(
                        process_run, engine, settings, settings.dev_tenant, run
                    )
                    active[future] = run
                if not lease:
                    time.sleep(1)
            except Exception:
                # Exception text/SQL may contain clinical payloads. Emit only a
                # stable operational code; the lease makes failed work recoverable.
                logging.error("worker_stage_failed")
                time.sleep(2)
    finally:
        # unfinished runs go back to the queue at once; the next worker resumes them from the
        # model cache (the stopped worker's own calls finish into the cache but cannot publish)
        for future, run in active.items():
            if not future.done():
                try:
                    release_run(engine, settings.dev_tenant, run)
                except Exception:
                    logging.error("worker_release_failed")
        executor.shutdown(wait=False, cancel_futures=True)
        engine.dispose()


if __name__ == "__main__":
    main()

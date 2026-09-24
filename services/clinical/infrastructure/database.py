from collections.abc import Iterator
from contextlib import contextmanager
from uuid import UUID

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session


def make_engine(url: str) -> Engine:
    return create_engine(url, pool_pre_ping=True, pool_size=5, max_overflow=5, hide_parameters=True)


@contextmanager
def transaction(engine: Engine, tenant_id: UUID) -> Iterator[Session]:
    with Session(engine, expire_on_commit=False) as session, session.begin():
        session.execute(
            text("SELECT set_config('app.tenant_id', :tenant, true)"), {"tenant": str(tenant_id)}
        )
        yield session

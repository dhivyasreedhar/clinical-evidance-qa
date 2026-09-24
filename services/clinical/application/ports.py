from typing import Protocol
from uuid import UUID


class ObjectStore(Protocol):
    def put(self, tenant_id: UUID, raw: bytes) -> str: ...

    def get(self, tenant_id: UUID, digest: str) -> bytes: ...

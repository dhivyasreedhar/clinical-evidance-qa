import hashlib
import os
import re
import tempfile
from pathlib import Path
from uuid import UUID


class LocalObjectStore:
    """Private development adapter. Atomic immutable publication; verifies reads."""

    def __init__(self, root: Path):
        self.root = root

    def _path(self, tenant_id: UUID, digest: str) -> Path:
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError("invalid_object_hash")
        return self.root / str(tenant_id) / digest[:2] / digest

    def put(self, tenant_id: UUID, raw: bytes) -> str:
        digest = hashlib.sha256(raw).hexdigest()
        path = self._path(tenant_id, digest)
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        fd, temporary = tempfile.mkstemp(dir=path.parent)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            try:
                os.link(temporary, path)
            except FileExistsError:
                if self.get(tenant_id, digest) != raw:
                    raise ValueError("object_integrity_failure") from None
        finally:
            os.unlink(temporary)
        return digest

    def get(self, tenant_id: UUID, digest: str) -> bytes:
        raw = self._path(tenant_id, digest).read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError("object_integrity_failure")
        return raw

import secrets
from dataclasses import dataclass
from uuid import UUID

from fastapi import HTTPException, Request
from itsdangerous import BadSignature, URLSafeTimedSerializer

from clinical.infrastructure.config import Settings

COOKIE = "ehr_dev_session"


@dataclass(frozen=True)
class Principal:
    tenant_id: UUID
    actor_id: UUID
    csrf: str


def serializer(settings: Settings) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(settings.session_secret, salt="ehr-development-session-v1")


def principal(request: Request) -> Principal:
    settings: Settings = request.app.state.settings
    try:
        data = serializer(settings).loads(request.cookies.get(COOKIE, ""), max_age=8 * 3600)
        result = Principal(UUID(data["tenant"]), UUID(data["actor"]), data["csrf"])
        if result.tenant_id != settings.dev_tenant or result.actor_id != settings.dev_actor:
            raise ValueError
    except (BadSignature, ValueError, KeyError, TypeError):
        raise HTTPException(401, detail="sign_in_required") from None
    if request.method not in {"GET", "HEAD", "OPTIONS"}:
        verify_origin(request)
        if not secrets.compare_digest(request.headers.get("x-csrf-token", ""), result.csrf):
            raise HTTPException(403, detail="csrf_failed")
    return result


def verify_origin(request: Request) -> None:
    settings: Settings = request.app.state.settings
    if request.headers.get("origin") != settings.browser_origin:
        raise HTTPException(403, detail="origin_not_allowed")

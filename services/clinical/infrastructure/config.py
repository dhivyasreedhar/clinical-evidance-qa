from pathlib import Path
from uuid import UUID

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="EHR_", env_file=".env", extra="ignore")
    environment: str = "development"
    database_url: str = "postgresql+psycopg://ehr_app:local-development@127.0.0.1:55432/ehr"
    migration_database_url: str = "postgresql+psycopg://ehr_owner:local-owner@127.0.0.1:55432/ehr"
    object_root: Path = Path(".local/objects")
    session_secret: str = Field(min_length=32)
    browser_origin: str = "http://localhost:3000"
    dev_tenant: UUID = UUID("11111111-1111-4111-8111-111111111111")
    dev_actor: UUID = UUID("22222222-2222-4222-8222-222222222222")
    max_file_bytes: int = 10 * 1024 * 1024
    max_import_bytes: int = 25 * 1024 * 1024
    max_files: int = 100
    # Passed to record_engine for its model calls (models: RECORD_ENGINE_WRITER / _SMALL).
    anthropic_api_key: SecretStr = SecretStr("")
    # Runs for different patients processed concurrently by one worker.
    run_concurrency: int = Field(default=2, ge=1, le=8)
    # Renewed every quarter lease while a run works; a stopped worker's runs resume after one lease.
    run_lease_seconds: int = Field(default=120, ge=60, le=900)

    @model_validator(mode="after")
    def development_only(self) -> "Settings":
        if self.environment not in {"development", "test"}:
            raise ValueError("Production is disabled until OIDC and release gates are implemented")
        if self.browser_origin not in {
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://testserver",
        } and not (self.environment == "test" and self.browser_origin == "http://localhost:3001"):
            raise ValueError("Development sign-in requires a loopback browser origin")
        return self

from alembic import context
from clinical.infrastructure.config import Settings
from clinical.infrastructure.models import Base
from sqlalchemy import create_engine

settings = Settings()
if context.is_offline_mode():
    context.configure(
        url=settings.migration_database_url, target_metadata=Base.metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()
else:
    engine = create_engine(settings.migration_database_url)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=Base.metadata)
        with context.begin_transaction():
            connection.exec_driver_sql("SELECT pg_advisory_xact_lock(8219301)")
            context.run_migrations()

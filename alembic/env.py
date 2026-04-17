import asyncio
from logging.config import fileConfig

from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool, text

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from app.core.config import config as app_cfg  # noqa: E402
from app.models.base import ModelBase  # noqa: E402
import app.models  # noqa: F401 E402

target_metadata = ModelBase.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


database_url = app_cfg.DATABASE_URL.get_secret_value()
config.set_main_option("sqlalchemy.url", database_url)

# ---------------------------------------------------------------------------
# Constraint naming conventions
#
# SQLAlchemy does not generate constraint names by default, which causes
# problems with Alembic when you need to DROP or ALTER a constraint —
# unnamed constraints cannot be referenced by name in DDL.
#
# This convention mirrors what is already set in the models (via
# __table_args__ UniqueConstraints with explicit names) and ensures
# any constraints Alembic generates automatically are also named.
# ---------------------------------------------------------------------------
naming_convention = {
    "ix": "ix_%(table_name)s_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def run_async_migrations() -> None:
        async with connectable.connect() as connection:
            await connection.run_sync(_run_migration_sync)

        await connectable.dispose()

    def _run_migration_sync(connection: Connection) -> None:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # Emit CREATE TYPE statements for SQLAlchemy Enum types.
            # Without this, Alembic won't create the PostgreSQL ENUM types
            # that back your Python enum columns (e.g. AssetType).
            include_schemas=True,
            # Compare server defaults so Alembic detects changes to
            # server_default values (e.g. func.now() on timestamp columns).
            compare_server_defaults=True,
            # Apply the naming convention so all generated constraints
            # have predictable, referenceable names.
            render_as_batch=False,  # batch mode is for SQLite only
            naming_convention=naming_convention,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

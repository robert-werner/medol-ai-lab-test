# migrations/env.py
import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# Import all models and Base
from app.db.models.orm.base import Base
from app.db.models.orm.user import User
from app.db.models.orm.token import Token
from app.db.models.orm.file_info import FileInfo
from app.settings import get_db_string

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata  # Must be set

# Async engine setup
url = get_db_string()
async_engine = create_async_engine(url)

def run_migrations_online():
    async def run_async_migrations():
        async with async_engine.connect() as connection:
            await connection.run_sync(do_run_migrations)
    asyncio.run(run_async_migrations())

def do_run_migrations(connection):

    context.configure(
        connection=connection,
        target_metadata=Base.metadata
    )
    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    # For offline mode, use a sync engine temporarily
    from sqlalchemy import create_engine
    sync_engine = create_engine(url.replace("+asyncpg", ""))  # Remove async driver
    with sync_engine.connect() as connection:
        do_run_migrations(connection)
else:
    run_migrations_online()
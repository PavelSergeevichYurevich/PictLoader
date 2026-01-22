from logging.config import fileConfig
from pathlib import Path
import sys
import asyncio

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.core.settings import settings
from app.models.base import Base

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
target_metadata = Base.metadata

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

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


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


import asyncio # Добавь в импорты в начало файла

def run_migrations_online() -> None:
    # 1. Создаем асинхронный движок
    from sqlalchemy.ext.asyncio import create_async_engine
    
    connectable = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    # 2. Внутренняя функция для выполнения миграций в синхронном контексте
    def do_run_migrations(connection):
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

    # 3. Запускаем асинхронный цикл
    async def run_async_migrations():
        async with connectable.connect() as connection:
            # Магия SQLAlchemy: запускаем синхронную функцию в асинхронном соединении
            await connection.run_sync(do_run_migrations)
        await connectable.dispose()

    # 4. Запускаем всё это дело
    asyncio.run(run_async_migrations())




if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

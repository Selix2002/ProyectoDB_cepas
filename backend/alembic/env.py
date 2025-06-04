# alembic/env.py

import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Importa aquí tu MetaData (igual que antes)
from app.models import Base

# Este es el objeto Config que Alembic carga del alembic.ini
config = context.config

# ---------------------------------------------------
# Lectura de DATABASE_URL para usar siempre psycopg2
db_url = os.getenv("DATABASE_URL")
if db_url:
    # Si la URL viene en formato "postgresql://...", forzamos "+psycopg2"
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
    # Sobreescribimos en la configuración de Alembic
    config.set_main_option("sqlalchemy.url", db_url)
# ---------------------------------------------------

# Configuración de logging (igual que antes)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Aquí definimos la MetaData de nuestro modelo para autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    Esto solo configura Alembic con la URL, sin crear un Engine físico.
    Ideal para generar SQL sin necesidad de tener el DBAPI cargado.
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
    """Run migrations en 'online' mode.

    En este modo Alembic crea un Engine y conecta directamente para aplicar migraciones.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


# Según el modo (offline/online) se llama a la función correspondiente
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# backend/app/main.py
import os
from pathlib import Path
from litestar import Litestar, get
from litestar.static_files import create_static_files_router
from litestar.config.cors import CORSConfig
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin, SQLAlchemySyncConfig
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin

from app.models import Base
from app.crud import CepaController

# 1. CORS como antes
cors = CORSConfig(
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["*"],
    allow_credentials=True,
)

# 2. Leemos la URL que definiste en Render (Internal Database URL)
db_url = os.getenv(
    "DATABASE_URL",
    # Fallback para tu entorno local:
    "postgresql+psycopg2://postgres:sebas@localhost/db_cepas"
)

# 3. Si la URL viene sin "+psycopg2", la convertimos para que SQLAlchemy
#    use explícitamente el driver psycopg2.
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

# 4. Configuramos SQLAlchemy con psycopg2
db_config = SQLAlchemySyncConfig(
    connection_string=db_url,
    create_all=True,          # o False si usas migraciones con Alembic
    metadata=Base.metadata,
)
sql_plugin = SQLAlchemyPlugin(config=db_config)

# 5. Router para estáticos (igual que antes)
static_router = create_static_files_router(
    path="/inicio",
    directories=[
        Path(__file__).resolve().parent.parent.parent / "frontend" / "public"
    ],
    html_mode=True,
)

@get(path="/")
def root() -> dict:
    return {"status": "ok", "message": "API de Cepas funcionando"}

# 6. Creamos la app Litestar
app = Litestar(
    route_handlers=[root,static_router, CepaController],
    openapi_config=OpenAPIConfig(
        title="Backend Cepas",
        description="API para la gestión de cepas",
        version="1.0.0",
        root_schema_site="scalar",
        render_plugins=[ScalarRenderPlugin()],
    ),
    plugins=[sql_plugin],
    cors_config=cors,
    debug=True,
)

# 7. Si ejecutas “python main.py” localmente, tomamos el puerto de Render
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,      # En producción puedes poner False
        app_dir="backend",
    )

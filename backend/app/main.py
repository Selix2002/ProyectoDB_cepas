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

cors = CORSConfig(
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Leemos DATABASE_URL y forzamos psycopg2 si hiciera falta
db_url = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:sebas@localhost/db_cepas")
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

db_config = SQLAlchemySyncConfig(
    connection_string=db_url,
    create_all=True,
    metadata=Base.metadata,
)
sql_plugin = SQLAlchemyPlugin(config=db_config)

static_router = create_static_files_router(
    path="/",  # opcional: monta tus archivos estáticos en "/"
    directories=[ Path(__file__).resolve().parent.parent.parent / "frontend" / "public" ],
    html_mode=True,
)

@get(path="/", methods=["GET", "HEAD"], sync_to_thread=False)
def root() -> dict:
    return {"status": "ok", "message": "API de Cepas funcionando"}

app = Litestar(
    route_handlers=[root, static_router, CepaController],
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

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        app_dir="backend",
    )

# backend/app/main.py
from pathlib import Path
from litestar import Litestar
from litestar.static_files import create_static_files_router
from litestar.config.cors import CORSConfig
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin, SQLAlchemySyncConfig
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin

from app.models import Base
from app.config import settings
from app.crud import CepaController

# 1) CORS a partir de env vars
cors = CORSConfig(
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
    allow_credentials=True,
)

# 2) Conexión a la DB desde env var DATABASE_URL
db_config = SQLAlchemySyncConfig(
    connection_string=settings.DATABASE_URL,
    create_all=True,
    metadata=Base.metadata,
)
sql_plugin = SQLAlchemyPlugin(config=db_config)

# 3) Static files (build de tu frontend), ruta y carpeta desde env vars
static_router = create_static_files_router(
    path=settings.FRONTEND_MOUNT_PATH,                           # e.g. "/"
    directories=[Path(settings.FRONTEND_BUILD_DIR)],              # e.g. "../frontend/dist"
    html_mode=True,                                               # sirve index.html para SPA
)

# 4) Montaje de la app
app = Litestar(
    route_handlers=[
        static_router,      # primero el frontend estático
        CepaController,     # luego tu API
    ],
    openapi_config=OpenAPIConfig(
        title="Backend Cepas",
        description="API para la gestión de cepas",
        version="1.0.0",
        root_schema_site="scalar",
        render_plugins=[ScalarRenderPlugin()],
    ),
    plugins=[sql_plugin],
    cors_config=cors,
    debug=settings.DEBUG,
)

# 5) Inicio con uvicorn usando host/port/debug desde env vars
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",       # módulo:app
        host=settings.HOST,   # e.g. "0.0.0.0"
        port=settings.PORT,   # e.g. 8000
        reload=settings.DEBUG,
        app_dir="backend",
    )

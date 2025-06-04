# backend/app/main.py
from pathlib import Path
from litestar import Litestar, get
from litestar.static_files import create_static_files_router
from litestar.config.cors import CORSConfig
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin, SQLAlchemySyncConfig
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from app.models import Base
from app.crud import (
    CepaController
)
# 1. Configuración CORS
cors = CORSConfig(
    allow_origins=["*"],        # en prod pon tu dominio, ej "https://midominio.com"
    allow_methods=["GET","POST","PATCH"],        # GET, POST, PUT, DELETE…
    allow_headers=["*"],        # Content-Type, Authorization…
    allow_credentials=True,
)

# 2. Plugin de SQLAlchemy (si lo usas)
db_config = SQLAlchemySyncConfig(
    connection_string="postgresql://sebas:EmqyWAorS6D1rekjwtkCvTmmmRtVew88@dpg-d104f4ali9vc73dfidag-a/cepas_db_ies3",
    create_all=True,
    metadata=Base.metadata,
)
sql_plugin = SQLAlchemyPlugin(config=db_config)

static_router = create_static_files_router(
    path="/inicio",
    directories=[
        Path(__file__).resolve().parent.parent.parent
        / "frontend"
        / "public"
    ],
    html_mode=True,  # al hacer GET /inicio sirve index.html automáticamente :contentReference[oaicite:1]{index=1}
)

# 3. Instancia de Litestar
app = Litestar(
    route_handlers=[static_router,CepaController],  # lista tus controllers o funciones route
    openapi_config=OpenAPIConfig(
        title="Backend Cepas",
        description="API para la gestión de cepas",
        version="1.0.0",
        root_schema_site="scalar",              # Usa Swagger UI como página raíz
        render_plugins=[ScalarRenderPlugin()],  # Solo carga el plugin de Swagger
    ),
    plugins=[sql_plugin],              # si no usas plugins, puedes omitir
    cors_config=cors,
    debug=True,
)


# 4. Permite arrancar levantando este archivo
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",         # módulo:path
        host="0.0.0.0",         # opcional
        port=8000,              # por defecto 8000
        reload=True,            # autoreload en desarrollo
        app_dir="backend",      # <--- MUY IMPORTANTE
    )

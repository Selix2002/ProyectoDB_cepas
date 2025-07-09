# backend/app/main.py
from pathlib import Path
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.static_files import create_static_files_router


from app.security import oauth2_auth
from app.db import db_config
from app.config import settings
from app.crud import (
    CepaController,
    UserController,
    AuthController,
)
# 1. Configuración CORS
cors = CORSConfig(
    allow_origins=["*"],        # en prod pon tu dominio, ej "https://midominio.com"
    allow_methods=["GET","POST","PATCH"],        # GET, POST, PUT, DELETE…
    allow_headers=["*"],        # Content-Type, Authorization…
    allow_credentials=True,
)

# 2. Configuración de la base de datos y OpenAPI
sql_plugin = SQLAlchemyPlugin(config=db_config)
openapi_config = OpenAPIConfig(
    title="Backend Cepas",
    description="API para la gestión de cepas",
    version="1.0.0",
    root_schema_site="scalar",  # para usar ScalarRenderPlugin
    render_plugins=[ScalarRenderPlugin()],  # para usar ScalarRenderPlugin
)
static_router = create_static_files_router(
    path=settings.FRONTEND_MOUNT_PATH,                           # e.g. "/"
    directories=[Path(settings.FRONTEND_BUILD_DIR)],              # e.g. "../frontend/dist"
    html_mode=True,                                               # sirve index.html para SPA
)

# 3. Instancia de Litestar
app = Litestar(
    route_handlers=[static_router,CepaController,UserController,AuthController],  # lista tus controllers o funciones route
    openapi_config=openapi_config,  # configuración de OpenAPI
    on_app_init=[oauth2_auth.on_app_init],  # inicializa el OAuth2 al arrancar la app
    plugins=[sql_plugin],              
    cors_config=cors,
    debug=settings.DEBUG,  # habilita el modo debug
)


# 4. Permite arrancar levantando este archivo
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",       # módulo:app
        host=settings.HOST,   # e.g. "0.0.0.0"
        port=settings.PORT,   # e.g. 8000
        reload=settings.DEBUG,
        app_dir="backend",
    )

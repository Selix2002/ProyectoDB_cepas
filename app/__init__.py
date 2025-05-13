from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base  # Asegúrate de importar tu Base
from app.crud import CepaController
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin, SQLAlchemySyncConfig
from litestar import Litestar
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin

db_config = SQLAlchemySyncConfig(
    connection_string="postgresql+psycopg2://postgres:sebas@localhost/db_cepas",create_all=True, metadata=Base.metadata
)
slqa_plugin = SQLAlchemyPlugin(config = db_config)
app = Litestar(
    route_handlers=[CepaController],plugins = [slqa_plugin],debug=True,
    openapi_config=OpenAPIConfig(
        title="Mi API",
        version="1.0.0",
        root_schema_site="swagger",              # Usa Swagger UI como página raíz
        render_plugins=[SwaggerRenderPlugin()],  # Solo carga el plugin de Swagger
    ),
)
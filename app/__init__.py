from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base  # Asegúrate de importar tu Base
from app.crud import CepaController
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin, SQLAlchemySyncConfig
from litestar import Litestar


db_config = SQLAlchemySyncConfig(
    connection_string="postgresql+psycopg2://postgres:sebas@localhost/db_cepas",create_all=True, metadata=Base.metadata
)
slqa_plugin = SQLAlchemyPlugin(config = db_config)
app = Litestar(
    route_handlers=[CepaController],plugins = [slqa_plugin],debug=True
)
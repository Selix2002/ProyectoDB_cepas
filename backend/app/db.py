from litestar.plugins.sqlalchemy import SQLAlchemySyncConfig

from app.config import settings
from app.models import Base

db_config = SQLAlchemySyncConfig(
    connection_string=settings.DATABASE_URL,
    create_all=True,
    metadata=Base.metadata,
)

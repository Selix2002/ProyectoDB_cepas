from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base  # Asegúrate de importar tu Base

# URL de conexión
DATABASE_URL = "postgresql+psycopg2://postgres:sebas@localhost/db_cepas"

# Crea el motor
engine = create_engine(DATABASE_URL)

# Sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas
def init_db():
    Base.metadata.create_all(bind=engine)

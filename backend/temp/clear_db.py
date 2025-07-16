import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# ------------------------------------------------------------------------
# Ajusta aquí tu URL de conexión si es necesario
# ------------------------------------------------------------------------
DATABASE_URL = "postgresql+psycopg2://sebas:ZpqBNF2Lr6xvM26JPTWMYA6cYR8tvvzh@dpg-d1nf2uidbo4c73eh9qk0-a/sebas_cepas_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def clear_all_tables():
    """
    Borra todos los registros de las tablas relacionadas con cepas
    y reinicia sus secuencias (autoincrementadores) a 1 usando TRUNCATE ... RESTART IDENTITY CASCADE.
    """
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                TRUNCATE TABLE
                    proyectos,
                    caracterizacion_genetica,
                    resistencia_antibiotica,
                    crecimiento_temperatura,
                    actividad_enzimatica,
                    morfologia,
                    medios_cultivo,
                    almacenamiento,
                    cepas
                RESTART IDENTITY CASCADE;
                """
            )
        )
    print("✅ Todas las tablas fueron truncadas y sus secuencias reiniciadas.")


if __name__ == "__main__":
    clear_all_tables()
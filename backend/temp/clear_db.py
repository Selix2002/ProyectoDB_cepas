import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# ------------------------------------------------------------------------
# Ajusta aquí tu URL de conexión si es necesario
# ------------------------------------------------------------------------
DATABASE_URL = "postgresql://sebas:EmqyWAorS6D1rekjwtkCvTmmmRtVew88@dpg-d104f4ali9vc73dfidag-a/cepas_db_ies3"
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

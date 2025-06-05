# backend/temp/load_data.py

import sys
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1) Directorio donde está este script:
THIS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))  
#    /opt/render/project/src/backend/temp

# 2) Subir un nivel para llegar a /opt/render/project/src/backend
BACKEND_DIR = os.path.abspath(os.path.join(THIS_FILE_DIR, os.pardir))  
#    /opt/render/project/src/backend

# 3) Agregar BACKEND_DIR al PYTHONPATH para poder hacer "from app.models import …"
sys.path.append(BACKEND_DIR)

# 4) Leer DATABASE_URL y forzar psycopg2 si hace falta
raw_db_url = os.getenv("DATABASE_URL")
if not raw_db_url:
    raise RuntimeError("La variable de entorno DATABASE_URL no está definida")
if raw_db_url.startswith("postgresql://"):
    db_url = raw_db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
else:
    db_url = raw_db_url

# 5) Crear engine y Session
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# 6) Importar los modelos desde app.models
from app.models import (
    Cepa,
    Almacenamiento,
    MedioCultivo,
    Morfologia,
    ActividadEnzimatica,
    CrecimientoTemperatura,
    ResistenciaAntibiotica,
    CaracterizacionGenetica,
    Proyecto,
)

# 7) Construir la ruta al CSV dentro de backend/data/…
csv_path = os.path.join(BACKEND_DIR, "data", "cepas_16_4_25.csv")
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"No se encontró el CSV en: {csv_path}")

# 8) Leer el CSV y rellenar valores nulos
df = pd.read_csv(csv_path)
df = df.fillna("N/I")

# 9) Iterar sobre cada fila e insertar en la base
for _, row in df.iterrows():
    cepa = Cepa(
        nombre=row["Cepa"],
        cod_lab=row["Cód-lab"],
        pigmentacion=row["Pigmentación"],
        origen=row["Origen"],
    )
    print(f"Procesando cepa: {cepa.nombre} ({cepa.cod_lab})")
    session.add(cepa)
    session.flush()  # para obtener cepa.id

    session.add(
        Almacenamiento(
            envio_puq=row["envio a PUQ"],
            temperatura_menos80=row["-80°"],
            cepa_id=cepa.id,
        )
    )
    session.add(MedioCultivo(medio=row["Medio Cultivo"], cepa_id=cepa.id))
    session.add(
        Morfologia(
            gram=row["Gram"],
            morfologia_1=row["morfologia"],
            morfologia_2=row["Morfologia"],
            cepa_id=cepa.id,
        )
    )
    session.add(
        ActividadEnzimatica(
            lecitinasa=row["Lecitinasa"],
            ureasa=row["Ureasa"],
            lipasa=row["Lipasa"],
            amilasa=row["Amilasa"],
            proteasa=row["Proteasa"],
            catalasa=row["Catalasa"],
            celulasa=row["Celulasa"],
            fosfatasa=row["Fosfatasa"],
            aia=row["AIA"],
            cepa_id=cepa.id,
        )
    )
    session.add(
        CrecimientoTemperatura(
            temp_5=row["5 ºC"],
            temp_25=row["25 °C"],
            temp_37=row["37 °C"],
            cepa_id=cepa.id,
        )
    )
    session.add(
        ResistenciaAntibiotica(
            amp=row["AMP"],
            ctx=row["CTX"],
            cxm=row["CXM"],
            caz=row["CAZ"],
            ak=row["AK"],
            c=row["C"],
            te=row["TE"],
            am_ecoli=row["AM E.coli"],
            am_saureus=row["AM S.aureus"],
            cepa_id=cepa.id,
        )
    )
    session.add(
        CaracterizacionGenetica(
            gen_16s=row["16S"], metabolomica=row["Metabolomica"], cepa_id=cepa.id
        )
    )
    session.add(
        Proyecto(
            responsable=row["Nicolás"],
            nombre_proyecto=row["Proyecto"],
            cepa_id=cepa.id,
        )
    )

session.commit()
session.close()
print("✅ Importación finalizada.")

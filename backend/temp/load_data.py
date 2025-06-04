# load_data.py (ubicado en backend/temp/load_data.py)

import sys
import os

# 1) CARPETA donde está load_data.py
THIS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))    # /opt/render/project/src/backend/temp

# 2) CARPETA “backend” real (dos niveles arriba de THIS_FILE_DIR)
BACKEND_DIR = os.path.abspath(os.path.join(THIS_FILE_DIR, os.pardir))  # /opt/render/project/src/backend

# 3) Ahora sí, agregamos BACKEND_DIR al PYTHONPATH
sys.path.append(BACKEND_DIR)

# — de aquí en adelante sigue tu lógica existente —
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 4) LEEMOS DATABASE_URL
raw_db_url = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:sebas@localhost/db_cepas"
)
if raw_db_url.startswith("postgresql://"):
    db_url = raw_db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
else:
    db_url = raw_db_url

# 5) CREAMOS ENGINE / SESSION
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

# 6) IMPORTAMOS LOS MODELOS (AHORA FUNCIONARÁ)
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

# 7) EL RESTO DE TU CÓDIGO DE INSERCIÓN…
csv_path = os.path.join(os.path.abspath(os.path.join(THIS_FILE_DIR, os.pardir, os.pardir)), "data", "cepas_16_4_25.csv")
df = pd.read_csv(csv_path)
df = df.fillna("N/I")

for _, row in df.iterrows():
    cepa = Cepa(
        nombre=row["Cepa"],
        cod_lab=row["Cód-lab"],
        pigmentacion=row["Pigmentación"],
        origen=row["Origen"],
    )
    print(f"Procesando cepa: {cepa.nombre} ({cepa.cod_lab})")
    session.add(cepa)
    session.flush()  # así tienes cepa.id

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
            temp_5=row["5 ºC"], temp_25=row["25 °C"], temp_37=row["37 °C"], cepa_id=cepa.id
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
            responsable=row["Nicolás"], nombre_proyecto=row["Proyecto"], cepa_id=cepa.id
        )
    )

session.commit()
session.close()
print("✅ Importación finalizada.")

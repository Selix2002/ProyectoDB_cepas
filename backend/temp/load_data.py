# load_data.py

import sys
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ————————————————
# 1) AÑADIMOS backend al PYTHONPATH
#    de forma que “from app.models import …” funcione correctamente.
#    Suponemos que este script está en la raíz del proyecto,
#    y que tu carpeta de código (“main.py”, “app/models.py”, etc.) está en “backend/app/”.
#————————————————————————
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))      # carpeta raíz del proyecto
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")            # ruta a /backend
sys.path.append(os.path.join(BACKEND_DIR))                 # añado “backend” al PYTHONPATH


# ————————————————
# 2) LEEMOS DATABASE_URL DESDE EL ENTORNO
#    Si se ha definido DATABASE_URL en Render (o en tu máquina local),
#    la usamos; si no existe, cae a un fallback local.
#————————————————————————
raw_db_url = os.getenv(
    "DATABASE_URL",
    # Fallback para desarrollo local, si no existe la var.:
    "postgresql+psycopg2://postgres:sebas@localhost/db_cepas"
)

# Forzamos psycopg2 si viene sin el sufijo:
if raw_db_url.startswith("postgresql://"):
    db_url = raw_db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
else:
    db_url = raw_db_url

# ————————————————
# 3) Creamos el engine y sessionmaker con SQLAlchemy
#————————————————————————
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()


# ————————————————
# 4) IMPORTAMOS NUESTROS MODELOS
#    Nota: ahora “backend” está en sys.path, así que “app.models” es válido.
#————————————————————————
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


# ————————————————
# 5) LEEMOS EL CSV
#    Suponemos que tienes un directorio “/data” en la raíz con el archivo.
#————————————————————————
csv_path = os.path.join(ROOT_DIR, "data", "cepas_16_4_25.csv")
df = pd.read_csv(csv_path)
df = df.fillna("N/I")


# ————————————————
# 6) RECORREMOS CADA FILA E INSERTAMOS EN BD
#————————————————————————
for _, row in df.iterrows():
    cepa = Cepa(
        nombre=row["Cepa"],
        cod_lab=row["Cód-lab"],
        pigmentacion=row["Pigmentación"],
        origen=row["Origen"],
    )
    print(f"Procesando cepa: {cepa.nombre} ({cepa.cod_lab})")
    session.add(cepa)
    session.flush()  # para que cepa.id esté disponible

    session.add(
        Almacenamiento(
            envio_puq=row["envio a PUQ"],
            temperatura_menos80=row["-80°"],
            cepa_id=cepa.id,
        )
    )
    session.add(
        MedioCultivo(medio=row["Medio Cultivo"], cepa_id=cepa.id)
    )
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

# ————————————————
# 7) COMIT Y CIERRE DE SESIÓN
#————————————————————————
session.commit()
session.close()
print("✅ Importación finalizada.")

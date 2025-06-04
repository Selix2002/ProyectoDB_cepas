import sys
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Agrega el directorio 'backend' al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Importa los modelos
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

# 1) Lee el CSV
csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cepas_16_4_25.csv")
df = pd.read_csv(csv_path)
df = df.fillna("N/I")
# 2) Conecta a la base
DATABASE_URL = "postgresql+psycopg2://postgres:sebas@localhost/db_cepas"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# 3) Procesa los datos
for _, row in df.iterrows():

    cepa = Cepa(
        nombre=row["Cepa"],
        cod_lab=row["Cód-lab"],
        pigmentacion=row["Pigmentación"],
        origen=row["Origen"],
    )
    print(f"Procesando cepa: {cepa.nombre} ({cepa.cod_lab})")
    session.add(cepa)
    session.flush()

    session.add(Almacenamiento(envio_puq=row["envio a PUQ"], temperatura_menos80=row["-80°"], cepa_id=cepa.id))
    session.add(MedioCultivo(medio=row["Medio Cultivo"], cepa_id=cepa.id))
    session.add(Morfologia(gram=row["Gram"], morfologia_1=row["morfologia"], morfologia_2=row["Morfologia"], cepa_id=cepa.id))
    session.add(ActividadEnzimatica(
        lecitinasa=row["Lecitinasa"], ureasa=row["Ureasa"], lipasa=row["Lipasa"],
        amilasa=row["Amilasa"], proteasa=row["Proteasa"], catalasa=row["Catalasa"],
        celulasa=row["Celulasa"], fosfatasa=row["Fosfatasa"], aia=row["AIA"], cepa_id=cepa.id,
    ))
    session.add(CrecimientoTemperatura(temp_5=row["5 ºC"], temp_25=row["25 °C"], temp_37=row["37 °C"], cepa_id=cepa.id))
    session.add(ResistenciaAntibiotica(
        amp=row["AMP"], ctx=row["CTX"], cxm=row["CXM"], caz=row["CAZ"], ak=row["AK"],
        c=row["C"], te=row["TE"], am_ecoli=row["AM E.coli"], am_saureus=row["AM S.aureus"], cepa_id=cepa.id,
    ))
    session.add(CaracterizacionGenetica(gen_16s=row["16S"], metabolomica=row["Metabolomica"], cepa_id=cepa.id))
    session.add(Proyecto(responsable=row["Nicolás"], nombre_proyecto=row["Proyecto"], cepa_id=cepa.id))

# 5) Guarda todo
session.commit()
session.close()
print("✅ Importación finalizada.")
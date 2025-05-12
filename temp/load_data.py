import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import (
    Base, Cepa, Almacenamiento, MedioCultivo, Morfologia,
    ActividadEnzimatica, CrecimientoTemperatura,
    ResistenciaAntibiotica, CaracterizacionGenetica, Proyecto
)

# 1) Lee el CSV
df = pd.read_csv('../data/cepas_16_4_25.csv')

# 2) Conecta a la base
DATABASE_URL = "postgresql+psycopg2://postgres:sebas@localhost/db_cepas"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

for _, row in df.iterrows():
    # Construyo primero el dict crudo
    raw_extra = {
        '16S': row.get('16S'),
        'Metabolomica': row.get('Metabolomica'),
        'responsable': row.get('Nicolás'),
        'proyecto': row.get('Proyecto')
    }
    # Ahora paso NaN a None
    datos_extra = {k: (None if pd.isna(v) else v) for k, v in raw_extra.items()}

    cepa = Cepa(
        nombre=row['Cepa'],
        cod_lab=row['Cód-lab'],
        pigmentacion=row['Pigmentación'],
        origen=row['Origen'],
        datos_extra=datos_extra
    )
    session.add(cepa)
    session.flush()

    # 4) Cada subtabla
    session.add(Almacenamiento(
        envio_puq=row['envio a PUQ'],
        temperatura_menos80=row['-80°'],
        cepa_id=cepa.id
    ))
    session.add(MedioCultivo(
        medio=row['Medio Cultivo'],
        cepa_id=cepa.id
    ))
    session.add(Morfologia(
        gram=row['Gram'],
        morfologia_1=row['morfologia'],
        morfologia_2=row['Morfologia'],
        cepa_id=cepa.id
    ))
    session.add(ActividadEnzimatica(
        lecitinasa=row['Lecitinasa'], ureasa=row['Ureasa'],
        lipasa=row['Lipasa'], amilasa=row['Amilasa'],
        proteasa=row['Proteasa'], catalasa=row['Catalasa'],
        celulasa=row['Celulasa'], fosfatasa=row['Fosfatasa'],
        aia=row['AIA'], cepa_id=cepa.id
    ))
    session.add(CrecimientoTemperatura(
        temp_5=row['5 ºC'], temp_25=row['25 °C'],
        temp_37=row['37 °C'], cepa_id=cepa.id
    ))
    session.add(ResistenciaAntibiotica(
        amp=row['AMP'], ctx=row['CTX'], cxm=row['CXM'],
        caz=row['CAZ'], ak=row['AK'], c=row['C'],
        te=row['TE'], am_ecoli=row['AM E.coli'],
        am_saureus=row['AM S.aureus'], cepa_id=cepa.id
    ))
    session.add(CaracterizacionGenetica(
        gen_16s=row['16S'], metabolomica=row['Metabolomica'],
        cepa_id=cepa.id
    ))
    session.add(Proyecto(
        responsable=row['Nicolás'], nombre_proyecto=row['Proyecto'],
        cepa_id=cepa.id
    ))

# 5) Guarda todo
session.commit()
session.close()
print("✅ Importación finalizada.")
s
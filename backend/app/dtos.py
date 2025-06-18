from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig
from app.models import Cepa, Almacenamiento, MedioCultivo, Morfologia, ActividadEnzimatica, CrecimientoTemperatura, ResistenciaAntibiotica, CaracterizacionGenetica, Proyecto
excludes_id = [
    "almacenamiento.id",
    "medio_cultivo.id",
    "morfologia.id",
    "actividad_enzimatica.id",
    "crecimiento_temperatura.id",
    "resistencia_antibiotica.id",
    "caracterizacion_genetica.id",
    "proyecto.id"
    "almacenamiento.cepa_id",
    "medio_cultivo.cepa_id",
    "morfologia.cepa_id",
    "actividad_enzimatica.cepa_id",
    "crecimiento_temperatura.cepa_id",
    "resistencia_antibiotica.cepa_id",
    "caracterizacion_genetica.cepa_id",
    "proyecto.cepa_id"
]
excludes_tables = [
    "almacenamiento",
    "medio_cultivo",
    "morfologia",
    "actividad_enzimatica",
    "crecimiento_temperatura",  
    "resistencia_antibiotica",
    "caracterizacion_genetica",
    "proyecto"
]
# DTO GET ALL
class CepaReadDTO(SQLAlchemyDTO[Cepa]):
    config = SQLAlchemyDTOConfig(exclude=excludes_id,)

# DTOs para leer
class CepaFullReadDTO(SQLAlchemyDTO[Cepa]):
    config = SQLAlchemyDTOConfig(exclude=excludes_id)


# DTOs para crear
class CepaCreateDTO(SQLAlchemyDTO[Cepa]):
    config = SQLAlchemyDTOConfig(
        exclude=["id"],
        partial=True,
    )

# DTOs para actualizar
class CepaUpdateDTO(SQLAlchemyDTO[Cepa]):
    config = SQLAlchemyDTOConfig(
        partial=True,
        exclude=excludes_id + ["id"] 
    )

#DTO para actualizar el JSONB de cepa
class CepaUpdateJSONBDTO(SQLAlchemyDTO[Cepa]):
    config = SQLAlchemyDTOConfig(exclude=excludes_tables + ["id","nombre","cod_lab","pigmentacion","origen"], partial=True)


    
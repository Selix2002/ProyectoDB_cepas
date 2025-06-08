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
        exclude=["id","almacenamiento.id"],
        partial=True,
    )

# DTOs para actualizar
class CepaUpdateDTO(SQLAlchemyDTO[Cepa]):
    config = SQLAlchemyDTOConfig(exclude=excludes_id + ["id"], partial=True)

#DTO para actualizar el JSONB de cepa
class CepaUpdateJSONBDTO(SQLAlchemyDTO[Cepa]):
    config = SQLAlchemyDTOConfig(exclude=excludes_tables + ["id","nombre","cod_lab","pigmentacion","origen"], partial=True)


    
from typing import Optional
from litestar.plugins.sqlalchemy import SQLAlchemyDTO
from advanced_alchemy.extensions.litestar import SQLAlchemyDTOConfig
from app.models import Cepa, Almacenamiento, MedioCultivo, Morfologia, ActividadEnzimatica, CrecimientoTemperatura, ResistenciaAntibiotica, CaracterizacionGenetica, Proyecto
from sqlalchemy import Update

# DTOs para crear
class CepaCreateDTO(SQLAlchemyDTO[Cepa]):
    config = SQLAlchemyDTOConfig(exclude=["id","almacenamiento", "medio_cultivo", "morfologia", "actividad_enzimatica", "crecimiento_temperatura", "resistencia_antibiotica", "caracterizacion_genetica", "proyecto"])
class AlmacenamientoCreateDTO(SQLAlchemyDTO[Almacenamiento]):
    config=SQLAlchemyDTOConfig(exclude={"id","cepa"})
class MedioCultivoCreateDTO(SQLAlchemyDTO[MedioCultivo]):
    config=SQLAlchemyDTOConfig(exclude={"id","cepa"})
class MorfologiaCreateDTO(SQLAlchemyDTO[Morfologia]):
    config=SQLAlchemyDTOConfig(exclude={"id","cepa"})
class ActividadEnzimaticaCreateDTO(SQLAlchemyDTO[ActividadEnzimatica]):
    config=SQLAlchemyDTOConfig(exclude={"id","cepa"})
class CrecimientoTemperaturaCreateDTO(SQLAlchemyDTO[CrecimientoTemperatura]):
    config=SQLAlchemyDTOConfig(exclude={"id","cepa"})
class ResistenciaAntibioticaCreateDTO(SQLAlchemyDTO[ResistenciaAntibiotica]):
    config=SQLAlchemyDTOConfig(exclude={"id","cepa"})
class CaracterizacionGeneticaCreateDTO(SQLAlchemyDTO[CaracterizacionGenetica]):
    config=SQLAlchemyDTOConfig(exclude={"id","cepa"})
class ProyectoCreateDTO(SQLAlchemyDTO[Proyecto]):
    config=SQLAlchemyDTOConfig(exclude={"id","cepa"})

# DTOs para leer
class CepaReadDTO(SQLAlchemyDTO[Cepa]):
    config = SQLAlchemyDTOConfig(exclude=["almacenamiento", "medio_cultivo", "morfologia", "actividad_enzimatica", "crecimiento_temperatura", "resistencia_antibiotica", "caracterizacion_genetica", "proyecto"])
class AlmacenamientoReadDTO(SQLAlchemyDTO[Almacenamiento]):
    config = SQLAlchemyDTOConfig(exclude=["cepa"])
    pass
class MedioCultivoReadDTO(SQLAlchemyDTO[MedioCultivo]):
    config = SQLAlchemyDTOConfig(exclude=["cepa"])
class MorfologiaReadDTO(SQLAlchemyDTO[Morfologia]):         
    config = SQLAlchemyDTOConfig(exclude=["cepa"])
class ActividadEnzimaticaReadDTO(SQLAlchemyDTO[ActividadEnzimatica]):
    config = SQLAlchemyDTOConfig(exclude=["cepa"])
class CrecimientoTemperaturaReadDTO(SQLAlchemyDTO[CrecimientoTemperatura]):
    config = SQLAlchemyDTOConfig(exclude=["cepa"])
class ResistenciaAntibioticaReadDTO(SQLAlchemyDTO[ResistenciaAntibiotica]):
    config = SQLAlchemyDTOConfig(exclude=["cepa"])
class CaracterizacionGeneticaReadDTO(SQLAlchemyDTO[CaracterizacionGenetica]):
    config = SQLAlchemyDTOConfig(exclude=["cepa"])
class ProyectoReadDTO(SQLAlchemyDTO[Proyecto]):
    config = SQLAlchemyDTOConfig(exclude=["cepa"])

# DTOs para actualizar
class CepaUpdateDTO(SQLAlchemyDTO[Update,Cepa]):
    config=SQLAlchemyDTOConfig(exclude={"id","almacenamiento", "medio_cultivo", "morfologia", "actividad_enzimatica", "crecimiento_temperatura", "resistencia_antibiotica", "caracterizacion_genetica", "proyecto"})
    nombre: Optional[str]
    cod_lab: Optional[str]
    pigmentacion: Optional[str]
    origen: Optional[str]
    datos_extra: Optional[dict]

class AlmacenamientoUpdateDTO(SQLAlchemyDTO[Almacenamiento]):
    config=SQLAlchemyDTOConfig(exclude={"id","cepa"})
class MedioCultivoUpdateDTO(SQLAlchemyDTO[MedioCultivo]):
    config=SQLAlchemyDTOConfig(exclude={"id","cepa"})
class MorfologiaUpdateDTO(SQLAlchemyDTO[Morfologia]):
    config=SQLAlchemyDTOConfig(exclude={"id","cepa"})      
class ActividadEnzimaticaUpdateDTO(SQLAlchemyDTO[ActividadEnzimatica]):
    config=SQLAlchemyDTOConfig(exclude={"id","cepa"})
class CrecimientoTemperaturaUpdateDTO(SQLAlchemyDTO[CrecimientoTemperatura]):
    config=SQLAlchemyDTOConfig(exclude={"id","cepa"})
class ResistenciaAntibioticaUpdateDTO(SQLAlchemyDTO[ResistenciaAntibiotica]):
    config=SQLAlchemyDTOConfig(exclude={"id","cepa"})
class CaracterizacionGeneticaUpdateDTO(SQLAlchemyDTO[CaracterizacionGenetica]):
    config=SQLAlchemyDTOConfig(exclude={"id","cepa"})
class ProyectoUpdateDTO(SQLAlchemyDTO[Proyecto]):
    config=SQLAlchemyDTOConfig(exclude={"id","cepa"})















from litestar.plugins.sqlalchemy import SQLAlchemyDTO
from advanced_alchemy.extensions.litestar import SQLAlchemyDTOConfig
from app.models import Cepa, Almacenamiento, MedioCultivo, Morfologia, ActividadEnzimatica, CrecimientoTemperatura, ResistenciaAntibiotica, CaracterizacionGenetica, Proyecto


# DTOs para crear
class CepaCreateDTO(SQLAlchemyDTO[Cepa]):
    config=SQLAlchemyDTOConfig(exclude={"id"})
class AlmacenamientoCreateDTO(SQLAlchemyDTO[Almacenamiento]):
    config=SQLAlchemyDTOConfig(exclude={"id"})
class MedioCultivoCreateDTO(SQLAlchemyDTO[MedioCultivo]):
    config=SQLAlchemyDTOConfig(exclude={"id"})
class MorfologiaCreateDTO(SQLAlchemyDTO[Morfologia]):
    config=SQLAlchemyDTOConfig(exclude={"id"})
class ActividadEnzimaticaCreateDTO(SQLAlchemyDTO[ActividadEnzimatica]):
    config=SQLAlchemyDTOConfig(exclude={"id"})
class CrecimientoTemperaturaCreateDTO(SQLAlchemyDTO[CrecimientoTemperatura]):
    config=SQLAlchemyDTOConfig(exclude={"id"})
class ResistenciaAntibioticaCreateDTO(SQLAlchemyDTO[ResistenciaAntibiotica]):
    config=SQLAlchemyDTOConfig(exclude={"id"})
class CaracterizacionGeneticaCreateDTO(SQLAlchemyDTO[CaracterizacionGenetica]):
    config=SQLAlchemyDTOConfig(exclude={"id"})
class ProyectoCreateDTO(SQLAlchemyDTO[Proyecto]):
    config=SQLAlchemyDTOConfig(exclude={"id"})

# DTOs para leer
class CepaReadDTO(SQLAlchemyDTO[Cepa]):
    config = SQLAlchemyDTOConfig(exclude=["almacenamiento", "medio_cultivo", "morfologia", "actividad_enzimatica", "crecimiento_temperatura", "resistencia_antibiotica", "caracterizacion_genetica", "proyecto"])

class AlmacenamientoReadDTO(SQLAlchemyDTO[Almacenamiento]):
    pass
class MedioCultivoReadDTO(SQLAlchemyDTO[MedioCultivo]):
    pass
class MorfologiaReadDTO(SQLAlchemyDTO[Morfologia]):         
    pass
class ActividadEnzimaticaReadDTO(SQLAlchemyDTO[ActividadEnzimatica]):
    pass
class CrecimientoTemperaturaReadDTO(SQLAlchemyDTO[CrecimientoTemperatura]):
    pass
class ResistenciaAntibioticaReadDTO(SQLAlchemyDTO[ResistenciaAntibiotica]):
    pass
class CaracterizacionGeneticaReadDTO(SQLAlchemyDTO[CaracterizacionGenetica]):
    pass
class ProyectoReadDTO(SQLAlchemyDTO[Proyecto]):
    pass

# DTOs para actualizar
class CepaUpdateDTO(SQLAlchemyDTO[Cepa]):
    config=SQLAlchemyDTOConfig(exclude={"id"})
class AlmacenamientoUpdateDTO(SQLAlchemyDTO[Almacenamiento]):
    config=SQLAlchemyDTOConfig(exclude={"id"})
class MedioCultivoUpdateDTO(SQLAlchemyDTO[MedioCultivo]):
    config=SQLAlchemyDTOConfig(exclude={"id"})
class MorfologiaUpdateDTO(SQLAlchemyDTO[Morfologia]):
    config=SQLAlchemyDTOConfig(exclude={"id"})      
class ActividadEnzimaticaUpdateDTO(SQLAlchemyDTO[ActividadEnzimatica]):
    config=SQLAlchemyDTOConfig(exclude={"id"})
class CrecimientoTemperaturaUpdateDTO(SQLAlchemyDTO[CrecimientoTemperatura]):
    config=SQLAlchemyDTOConfig(exclude={"id"})
class ResistenciaAntibioticaUpdateDTO(SQLAlchemyDTO[ResistenciaAntibiotica]):
    config=SQLAlchemyDTOConfig(exclude={"id"})
class CaracterizacionGeneticaUpdateDTO(SQLAlchemyDTO[CaracterizacionGenetica]):
    config=SQLAlchemyDTOConfig(exclude={"id"})
class ProyectoUpdateDTO(SQLAlchemyDTO[Proyecto]):
    config=SQLAlchemyDTOConfig(exclude={"id"})















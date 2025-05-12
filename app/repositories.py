from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy.orm import Session
from app.models import Cepa, Almacenamiento, MedioCultivo, Morfologia, ActividadEnzimatica, CrecimientoTemperatura, ResistenciaAntibiotica, CaracterizacionGenetica, Proyecto

class CepaRepository(SQLAlchemySyncRepository[Cepa]):
    model_type = Cepa
async def provide_cepa_repo(db_session: Session) -> CepaRepository:
    return CepaRepository(session=db_session)
class AlmacenamientoRepository(SQLAlchemySyncRepository[Almacenamiento]):
    model_type = Almacenamiento
async def provide_almacenamiento_repo(db_session: Session) -> AlmacenamientoRepository:
    return AlmacenamientoRepository(session=db_session)
class MedioCultivoRepository(SQLAlchemySyncRepository[MedioCultivo]):
    model_type = MedioCultivo
async def provide_medio_cultivo_repo(db_session: Session) -> MedioCultivoRepository:
    return MedioCultivoRepository(session=db_session)
class MorfologiaRepository(SQLAlchemySyncRepository[Morfologia]):
    model_type = Morfologia
async def provide_morfologia_repo(db_session: Session) -> MorfologiaRepository:
    return MorfologiaRepository(session=db_session)
class ActividadEnzimaticaRepository(SQLAlchemySyncRepository[ActividadEnzimatica]):
    model_type = ActividadEnzimatica
async def provide_actividad_enzimatica_repo(db_session: Session) -> ActividadEnzimaticaRepository:
    return ActividadEnzimaticaRepository(session=db_session)
class CrecimientoTemperaturaRepository(SQLAlchemySyncRepository[CrecimientoTemperatura]):
    model_type = CrecimientoTemperatura
async def provide_crecimiento_temperatura_repo(db_session: Session) -> CrecimientoTemperaturaRepository:
    return CrecimientoTemperaturaRepository(session=db_session)
class ResistenciaAntibioticaRepository(SQLAlchemySyncRepository[ResistenciaAntibiotica]):
    model_type = ResistenciaAntibiotica
async def provide_resistencia_antibiotica_repo(db_session: Session) -> ResistenciaAntibioticaRepository:
    return ResistenciaAntibioticaRepository(session=db_session)
class CaracterizacionGeneticaRepository(SQLAlchemySyncRepository[CaracterizacionGenetica]):
    model_type = CaracterizacionGenetica
async def provide_caracterizacion_genetica_repo(db_session: Session) -> CaracterizacionGeneticaRepository:
    return CaracterizacionGeneticaRepository(session=db_session)
class ProyectoRepository(SQLAlchemySyncRepository[Proyecto]):
    model_type = Proyecto
async def provide_proyecto_repo(db_session: Session) -> ProyectoRepository:
    return ProyectoRepository(session=db_session)
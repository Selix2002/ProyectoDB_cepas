from typing import Sequence
from litestar import Controller, get, post, patch, delete
from litestar.exceptions import HTTPException
from advanced_alchemy.exceptions import NotFoundError
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from advanced_alchemy.filters import ComparisonFilter
from sqlalchemy.orm import Session
from litestar.dto import DTOData
from litestar.di import Provide
from app.repositories import (
    CepaRepository,
    AlmacenamientoRepository,
    MedioCultivoRepository,
    MorfologiaRepository,
    ActividadEnzimaticaRepository,
    CrecimientoTemperaturaRepository,
    ResistenciaAntibioticaRepository,
    CaracterizacionGeneticaRepository,
    ProyectoRepository,
    provide_cepa_repo,
    provide_actividad_enzimatica_repo,
    provide_almacenamiento_repo,
    provide_caracterizacion_genetica_repo,
    provide_crecimiento_temperatura_repo,
    provide_medio_cultivo_repo,
    provide_morfologia_repo,
    provide_proyecto_repo,
    provide_resistencia_antibiotica_repo
)
from app.dtos import (
    CepaCreateDTO,
    AlmacenamientoCreateDTO,
    MedioCultivoCreateDTO,
    MorfologiaCreateDTO,
    ActividadEnzimaticaCreateDTO,
    CrecimientoTemperaturaCreateDTO,
    ResistenciaAntibioticaCreateDTO,
    CaracterizacionGeneticaCreateDTO,
    ProyectoCreateDTO,

    CepaReadDTO,
    AlmacenamientoReadDTO,
    MedioCultivoReadDTO,
    MorfologiaReadDTO,
    ActividadEnzimaticaReadDTO,
    CrecimientoTemperaturaReadDTO,
    ResistenciaAntibioticaReadDTO,
    CaracterizacionGeneticaReadDTO,
    ProyectoReadDTO,
    
    CepaUpdateDTO,
    AlmacenamientoUpdateDTO,
    MedioCultivoUpdateDTO,
    MorfologiaUpdateDTO,
    ActividadEnzimaticaUpdateDTO,
    CrecimientoTemperaturaUpdateDTO,
    ResistenciaAntibioticaUpdateDTO,
    CaracterizacionGeneticaUpdateDTO,
    ProyectoUpdateDTO
)
from app.models import (
    Cepa,
    Almacenamiento,
    MedioCultivo,
    Morfologia,
    ActividadEnzimatica,
    CrecimientoTemperatura,
    ResistenciaAntibiotica,
    CaracterizacionGenetica,
    Proyecto
)


class CepaController(Controller):
    path = "/cepas"
    tags = ["Cepa"]
    dto = CepaReadDTO
    dependencies = {
        "cepa_repo": Provide(provide_cepa_repo),
    }
    
    @get("/")
    async def get_all(self, cepa_repo: CepaRepository) -> Sequence[Cepa]:
        """
        Devuelve todas las instancias de Cepa.
        Gracias a `dto = CepaReadDTO`, Litestar convierte cada entidad
        a su DTO correspondiente y luego serializa a JSON.
        """
        return cepa_repo.list()
    @post("/", dto=CepaCreateDTO) #CREATE
    async def add_cepa(self,cepa_repo: CepaRepository,data: Cepa) -> Sequence[Cepa]:
        nueva = cepa_repo.add(data, auto_commit=True)
        return [nueva]

class AlmacenamientoController(Controller):
    path = "/almacenamiento"
    tags = ["Almacenamiento"]
    dto = AlmacenamientoReadDTO
    dependencies = {
        "almacenamiento_repo": Provide(provide_almacenamiento_repo),
    }
    
    @get("/")
    async def get_all(self, almacenamiento_repo: AlmacenamientoRepository) -> Sequence[Almacenamiento]:
        """
        Devuelve todas las instancias de Almacenamiento.
        Gracias a `dto = AlmacenamientoReadDTO`, Litestar convierte cada entidad
        a su DTO correspondiente y luego serializa a JSON.
        """
        return almacenamiento_repo.list()
    @post("/", dto=AlmacenamientoCreateDTO) #CREATE
    async def add_almacenamiento(self,almacenamiento_repo: AlmacenamientoRepository,data: Almacenamiento) -> Sequence[Almacenamiento]:
        nueva = almacenamiento_repo.add(data, auto_commit=True)
        return [nueva]
class MedioCultivoController(Controller):
    path = "/medios_cultivo"
    tags = ["MedioCultivo"]
    dto = MedioCultivoReadDTO
    dependencies = {
        "medio_cultivo_repo": Provide(provide_medio_cultivo_repo),
    }
     
    @get("/")
    async def get_all(self, medio_cultivo_repo: MedioCultivoRepository) -> Sequence[MedioCultivo]:
        """
        Devuelve todas las instancias de MedioCultivo.
        Gracias a `dto = MedioCultivoReadDTO`, Litestar convierte cada entidad
        a su DTO correspondiente y luego serializa a JSON.
        """
        return medio_cultivo_repo.list()
    @post("/", dto=MedioCultivoCreateDTO) #CREATE
    async def add_medio(self,medio_cultivo_repo: MedioCultivoRepository,data: MedioCultivo) -> Sequence[MedioCultivo]:
        nueva = medio_cultivo_repo.add(data, auto_commit=True)
        return [nueva]
class MorfologiaController(Controller):
    path = "/morfologia"
    tags = ["Morfologia"]
    dto = MorfologiaReadDTO
    dependencies = {
        "morfologia_repo": Provide(provide_morfologia_repo),
    }
    
    @get("/")
    async def get_all(self, morfologia_repo: MorfologiaRepository) -> Sequence[Morfologia]:
        """
        Devuelve todas las instancias de Morfologia.
        Gracias a `dto = MorfologiaReadDTO`, Litestar convierte cada entidad
        a su DTO correspondiente y luego serializa a JSON.
        """
        return morfologia_repo.list()
    @post("/", dto=MorfologiaCreateDTO) #CREATE
    async def add_morfologia(self,morfologia_repo: MorfologiaRepository,data: Morfologia) -> Sequence[Morfologia]:
        nueva = morfologia_repo.add(data, auto_commit=True)
        return [nueva]
class ActividadEnzimaticaController(Controller):
    path = "/actividad_enzimatica"
    tags = ["ActividadEnzimatica"]
    dto = ActividadEnzimaticaReadDTO
    dependencies = {
        "actividad_enzimatica_repo": Provide(provide_actividad_enzimatica_repo),
    }
    
    @get("/")
    async def get_all(self, actividad_enzimatica_repo: ActividadEnzimaticaRepository) -> Sequence[ActividadEnzimatica]:
        """
        Devuelve todas las instancias de ActividadEnzimatica.
        Gracias a `dto = ActividadEnzimaticaReadDTO`, Litestar convierte cada entidad
        a su DTO correspondiente y luego serializa a JSON.
        """
        return actividad_enzimatica_repo.list()
    @post("/", dto=ActividadEnzimaticaCreateDTO) #CREATE
    async def add_actividad(self,actividad_enzimatica_repo: ActividadEnzimaticaRepository,data: ActividadEnzimatica) -> Sequence[ActividadEnzimatica]:
        nueva = actividad_enzimatica_repo.add(data, auto_commit=True)
        return [nueva]
class CrecimientoTemperaturaController(Controller):
    path = "/crecimiento_temperatura"
    tags = ["CrecimientoTemperatura"]
    dto = CrecimientoTemperaturaReadDTO
    dependencies = {
        "crecimiento_temperatura_repo": Provide(provide_crecimiento_temperatura_repo),
    }
    
    @get("/")
    async def get_all(self, crecimiento_temperatura_repo: CrecimientoTemperaturaRepository) -> Sequence[CrecimientoTemperatura]:
        """
        Devuelve todas las instancias de CrecimientoTemperatura.
        Gracias a `dto = CrecimientoTemperaturaReadDTO`, Litestar convierte cada entidad
        a su DTO correspondiente y luego serializa a JSON.
        """
        return crecimiento_temperatura_repo.list()
    @post("/", dto=CrecimientoTemperaturaCreateDTO) #CREATE
    async def add_crecimiento(self,crecimiento_temperatura_repo: CrecimientoTemperaturaRepository,data: CrecimientoTemperatura) -> Sequence[CrecimientoTemperatura]:
        nueva = crecimiento_temperatura_repo.add(data, auto_commit=True)
        return [nueva]
class ResistenciaAntibioticaController(Controller):
    path = "/resistencia_antibiotica"
    tags = ["ResistenciaAntibiotica"]
    dto = ResistenciaAntibioticaReadDTO
    dependencies = {
        "resistencia_antibiotica_repo": Provide(provide_resistencia_antibiotica_repo),
    }
    
    @get("/")
    async def get_all(self, resistencia_antibiotica_repo: ResistenciaAntibioticaRepository) -> Sequence[ResistenciaAntibiotica]:
        """
        Devuelve todas las instancias de ResistenciaAntibiotica.
        Gracias a `dto = ResistenciaAntibioticaReadDTO`, Litestar convierte cada entidad
        a su DTO correspondiente y luego serializa a JSON.
        """
        return resistencia_antibiotica_repo.list()
    @post("/", dto=ResistenciaAntibioticaCreateDTO) #CREATE
    async def add_resistencia(self,resistencia_antibiotica_repo: ResistenciaAntibioticaRepository,data: ResistenciaAntibiotica) -> Sequence[ResistenciaAntibiotica]:
        nueva = resistencia_antibiotica_repo.add(data, auto_commit=True)
        return [nueva]
class CaracterizacionGeneticaController(Controller):
    path = "/caracterizacion_genetica"
    tags = ["CaracterizacionGenetica"]
    dto = CaracterizacionGeneticaReadDTO
    dependencies = {
        "caracterizacion_genetica_repo": Provide(provide_caracterizacion_genetica_repo),
    }
    
    @get("/")
    async def get_all(self, caracterizacion_genetica_repo: CaracterizacionGeneticaRepository) -> Sequence[CaracterizacionGenetica]:
        """
        Devuelve todas las instancias de CaracterizacionGenetica.
        Gracias a `dto = CaracterizacionGeneticaReadDTO`, Litestar convierte cada entidad
        a su DTO correspondiente y luego serializa a JSON.
        """
        return caracterizacion_genetica_repo.list()
    @post("/", dto=CaracterizacionGeneticaCreateDTO) #CREATE
    async def add_caracterizacion(self,caracterizacion_genetica_repo: CaracterizacionGeneticaRepository,data: CaracterizacionGenetica) -> Sequence[CaracterizacionGenetica]:
        nueva = caracterizacion_genetica_repo.add(data, auto_commit=True)
        return [nueva]
class ProyectoController(Controller):
    path = "/proyectos"
    tags = ["Proyecto"]
    dto = ProyectoReadDTO
    dependencies = {
        "proyecto_repo": Provide(provide_proyecto_repo),
    }
    
    @get("/")
    async def get_all(self, proyecto_repo: ProyectoRepository) -> Sequence[Proyecto]:
        """
        Devuelve todas las instancias de Proyecto.
        Gracias a `dto = ProyectoReadDTO`, Litestar convierte cada entidad
        a su DTO correspondiente y luego serializa a JSON.
        """
        return proyecto_repo.list()
    @post("/", dto=ProyectoCreateDTO) #CREATE
    async def add_proyecto(self,proyecto_repo: ProyectoRepository,data: Proyecto) -> Sequence[Proyecto]:
        nueva = proyecto_repo.add(data, auto_commit=True)
        return [nueva]
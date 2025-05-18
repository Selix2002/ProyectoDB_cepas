from typing import Sequence
from typing import Any
from litestar import Controller, get, post, patch, delete
from litestar.exceptions import HTTPException
from advanced_alchemy.exceptions import NotFoundError
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from advanced_alchemy.filters import ComparisonFilter
from sqlalchemy.orm import Session
from litestar.dto import DTOData
from litestar.di import Provide
from litestar import get, Request
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
    @get("/get-all")
    async def get_all(self, cepa_repo: CepaRepository) -> Sequence[Cepa]:
        """
        Devuelve todas las instancias de Cepa.
        Gracias a `dto = CepaReadDTO`, Litestar convierte cada entidad
        a su DTO correspondiente y luego serializa a JSON.
        """
        return cepa_repo.list()
    @post("/create", dto=CepaCreateDTO) #CREATE
    async def add_cepa(self,cepa_repo: CepaRepository,data: Cepa) -> Sequence[Cepa]:
        nueva = cepa_repo.add(data, auto_commit=True)
        return [nueva]
    @patch("/{cepa_id:int}", dto=CepaUpdateDTO)     #UPDATE PARA MODIFICAR UNO O MAS CAMPOS
    async def update_cepa(self,cepa_repo: CepaRepository,cepa_id: int,data: DTOData[Cepa],) -> Cepa:
        # 1. Obtenemos el dict completo
        all_updates = data.as_builtins()
        # 2. Quitamos las claves cuyo valor es None
        updates = {k: v for k, v in all_updates.items() if v is not None}

        # 3. Llamamos al repositorio sólo con los campos que realmente queremos cambiar
        updated_cepa, _ = cepa_repo.get_and_update(
           match_fields=["id"],
            id=cepa_id,
            **updates,
            auto_commit=True,
        )
        return updated_cepa
    #Un select con filtros
    @get("/list-cepa")
    async def list_cepas(self,cepa_repo: CepaRepository,request: Request) -> list[Cepa]:
        # 1. Leer todos los query params
        raw_filters: dict[str, Any] = dict(request.query_params)

        # 2. (Opcional) quedarnos sólo con los campos válidos del modelo
        valid_fields = set(Cepa.__table__.columns.keys())
        filtros = {
            k: v
            for k, v in raw_filters.items()
            if k in valid_fields
        }

        # 3. Llamar al repositorio
        return cepa_repo.find_many(
            match_fields=list(filtros.keys()),
            **filtros
        )

class AlmacenamientoController(Controller):
    path = "/almacenamiento"
    tags = ["Almacenamiento"]
    dto = AlmacenamientoReadDTO
    dependencies = {
        "almacenamiento_repo": Provide(provide_almacenamiento_repo),
    }  
    @get("/get-all")
    async def get_all(self, almacenamiento_repo: AlmacenamientoRepository) -> Sequence[Almacenamiento]:
        """
        Devuelve todas las instancias de Almacenamiento.
        Gracias a `dto = AlmacenamientoReadDTO`, Litestar convierte cada entidad
        a su DTO correspondiente y luego serializa a JSON.
        """
        return almacenamiento_repo.list()
    @post("/create", dto=AlmacenamientoCreateDTO) #CREATE
    async def add_almacenamiento(self,almacenamiento_repo: AlmacenamientoRepository,data: Almacenamiento) -> Sequence[Almacenamiento]:
        nueva = almacenamiento_repo.add(data, auto_commit=True)
        return [nueva]
    @patch("/{almacenamiento_id:int}", dto=AlmacenamientoUpdateDTO)
    async def update_almacenamiento(self,almacenamiento_repo: AlmacenamientoRepository,almacenamiento_id: int,data: DTOData[Almacenamiento],) -> Almacenamiento:
        all_updates = data.as_builtins()
        updates = {k: v for k, v in all_updates.items() if v is not None}
        updated_almacenamiento, _ = almacenamiento_repo.get_and_update(
            match_fields=["id"],
            id=almacenamiento_id,
            **updates,
            auto_commit=True,
        )
        return updated_almacenamiento
    @get("/list-almacenamiento")
    async def list_almacenamientos(self,almacenamiento_repo: AlmacenamientoRepository,request: Request) -> list[Almacenamiento]:
        # 1. Leer todos los query params
        raw_filters: dict[str, Any] = dict(request.query_params)

        # 2. (Opcional) quedarnos sólo con los campos válidos del modelo
        valid_fields = set(Almacenamiento.__table__.columns.keys())
        filtros = {
            k: v
            for k, v in raw_filters.items()
            if k in valid_fields
        }

        # 3. Llamar al repositorio
        return almacenamiento_repo.find_many(
            match_fields=list(filtros.keys()),
            **filtros
        )
class MedioCultivoController(Controller):
    path = "/medios_cultivo"
    tags = ["MedioCultivo"]
    dto = MedioCultivoReadDTO
    dependencies = {
        "medio_cultivo_repo": Provide(provide_medio_cultivo_repo),
    }
     
    @get("/get-all")
    async def get_all(self, medio_cultivo_repo: MedioCultivoRepository) -> Sequence[MedioCultivo]:
        """
        Devuelve todas las instancias de MedioCultivo.
        Gracias a `dto = MedioCultivoReadDTO`, Litestar convierte cada entidad
        a su DTO correspondiente y luego serializa a JSON.
        """
        return medio_cultivo_repo.list()
    @post("/create", dto=MedioCultivoCreateDTO) #CREATE
    async def add_medio(self,medio_cultivo_repo: MedioCultivoRepository,data: MedioCultivo) -> Sequence[MedioCultivo]:
        nueva = medio_cultivo_repo.add(data, auto_commit=True)
        return [nueva]
    @patch("/{medio_cultivo_id:int}", dto=MedioCultivoUpdateDTO)
    async def update_medio(self,medio_cultivo_repo: MedioCultivoRepository,medio_cultivo_id: int,data: DTOData[MedioCultivo],) -> MedioCultivo:
        all_updates = data.as_builtins()
        updates = {k: v for k, v in all_updates.items() if v is not None}
        updated_medio, _ = medio_cultivo_repo.get_and_update(
            match_fields=["id"],
            id=medio_cultivo_id,
            **updates,
            auto_commit=True,
        )
        return updated_medio
    @get("/list-medio_cultivo")
    async def list_medio_cultivos(self,medio_cultivo_repo: MedioCultivoRepository,request: Request) -> list[MedioCultivo]:
        # 1. Leer todos los query params
        raw_filters: dict[str, Any] = dict(request.query_params)

        # 2. (Opcional) quedarnos sólo con los campos válidos del modelo
        valid_fields = set(MedioCultivo.__table__.columns.keys())
        filtros = {
            k: v
            for k, v in raw_filters.items()
            if k in valid_fields
        }

        # 3. Llamar al repositorio
        return medio_cultivo_repo.find_many(
            match_fields=list(filtros.keys()),
            **filtros
        )
class MorfologiaController(Controller):
    path = "/morfologia"
    tags = ["Morfologia"]
    dto = MorfologiaReadDTO
    dependencies = {
        "morfologia_repo": Provide(provide_morfologia_repo),
    }
    
    @get("/get-all")
    async def get_all(self, morfologia_repo: MorfologiaRepository) -> Sequence[Morfologia]:
        """
        Devuelve todas las instancias de Morfologia.
        Gracias a `dto = MorfologiaReadDTO`, Litestar convierte cada entidad
        a su DTO correspondiente y luego serializa a JSON.
        """
        return morfologia_repo.list()
    @post("/create", dto=MorfologiaCreateDTO) #CREATE
    async def add_morfologia(self,morfologia_repo: MorfologiaRepository,data: Morfologia) -> Sequence[Morfologia]:
        nueva = morfologia_repo.add(data, auto_commit=True)
        return [nueva]
    @patch("/{morfologia_id:int}", dto=MorfologiaUpdateDTO)
    async def update_morfologia(self,morfologia_repo: MorfologiaRepository,morfologia_id: int,data: DTOData[Morfologia],) -> Morfologia:
        all_updates = data.as_builtins()
        updates = {k: v for k, v in all_updates.items() if v is not None}
        updated_morfologia, _ = morfologia_repo.get_and_update(
            match_fields=["id"],
            id=morfologia_id,
            **updates,
            auto_commit=True,
        )
        return updated_morfologia
    @get("/list-morfologia")
    async def list_morfologias(self,morfologia_repo: MorfologiaRepository,request: Request) -> list[Morfologia]:
        # 1. Leer todos los query params
        raw_filters: dict[str, Any] = dict(request.query_params)

        # 2. (Opcional) quedarnos sólo con los campos válidos del modelo
        valid_fields = set(Morfologia.__table__.columns.keys())
        filtros = {
            k: v
            for k, v in raw_filters.items()
            if k in valid_fields
        }

        # 3. Llamar al repositorio
        return morfologia_repo.find_many(
            match_fields=list(filtros.keys()),
            **filtros
        )

class ActividadEnzimaticaController(Controller):
    path = "/actividad_enzimatica"
    tags = ["ActividadEnzimatica"]
    dto = ActividadEnzimaticaReadDTO
    dependencies = {
        "actividad_enzimatica_repo": Provide(provide_actividad_enzimatica_repo),
    }
    
    @get("/get-all")
    async def get_all(self, actividad_enzimatica_repo: ActividadEnzimaticaRepository) -> Sequence[ActividadEnzimatica]:
        """
        Devuelve todas las instancias de ActividadEnzimatica.
        Gracias a `dto = ActividadEnzimaticaReadDTO`, Litestar convierte cada entidad
        a su DTO correspondiente y luego serializa a JSON.
        """
        return actividad_enzimatica_repo.list()
    @post("/create", dto=ActividadEnzimaticaCreateDTO) #CREATE
    async def add_actividad(self,actividad_enzimatica_repo: ActividadEnzimaticaRepository,data: ActividadEnzimatica) -> Sequence[ActividadEnzimatica]:
        nueva = actividad_enzimatica_repo.add(data, auto_commit=True)
        return [nueva]
    @patch("/{actividad_enzimatica_id:int}", dto=ActividadEnzimaticaUpdateDTO)
    async def update_actividad(self,actividad_enzimatica_repo: ActividadEnzimaticaRepository,actividad_enzimatica_id: int,data: DTOData[ActividadEnzimatica],) -> ActividadEnzimatica:
        all_updates = data.as_builtins()
        updates = {k: v for k, v in all_updates.items() if v is not None}
        updated_actividad, _ = actividad_enzimatica_repo.get_and_update(
            match_fields=["id"],
            id=actividad_enzimatica_id,
            **updates,
            auto_commit=True,
        )
        return updated_actividad
    @get("/list-actividad_enzimatica")
    async def list_actividad_enzimatica(self,actividad_enzimatica_repo: ActividadEnzimaticaRepository,request: Request) -> list[ActividadEnzimatica]:
        # 1. Leer todos los query params
        raw_filters: dict[str, Any] = dict(request.query_params)

        # 2. (Opcional) quedarnos sólo con los campos válidos del modelo
        valid_fields = set(ActividadEnzimatica.__table__.columns.keys())
        filtros = {
            k: v
            for k, v in raw_filters.items()
            if k in valid_fields
        }

        # 3. Llamar al repositorio
        return actividad_enzimatica_repo.find_many(
            match_fields=list(filtros.keys()),
            **filtros
        )
class CrecimientoTemperaturaController(Controller):
    path = "/crecimiento_temperatura"
    tags = ["CrecimientoTemperatura"]
    dto = CrecimientoTemperaturaReadDTO
    dependencies = {
        "crecimiento_temperatura_repo": Provide(provide_crecimiento_temperatura_repo),
    }
    
    @get("/get-all")
    async def get_all(self, crecimiento_temperatura_repo: CrecimientoTemperaturaRepository) -> Sequence[CrecimientoTemperatura]:
        """
        Devuelve todas las instancias de CrecimientoTemperatura.
        Gracias a `dto = CrecimientoTemperaturaReadDTO`, Litestar convierte cada entidad
        a su DTO correspondiente y luego serializa a JSON.
        """
        return crecimiento_temperatura_repo.list()
    @post("/create", dto=CrecimientoTemperaturaCreateDTO) #CREATE
    async def add_crecimiento(self,crecimiento_temperatura_repo: CrecimientoTemperaturaRepository,data: CrecimientoTemperatura) -> Sequence[CrecimientoTemperatura]:
        nueva = crecimiento_temperatura_repo.add(data, auto_commit=True)
        return [nueva]
    @patch("/{crecimiento_temperatura_id:int}", dto=CrecimientoTemperaturaUpdateDTO)
    async def update_crecimiento(self,crecimiento_temperatura_repo: CrecimientoTemperaturaRepository,crecimiento_temperatura_id: int,data: DTOData[CrecimientoTemperatura],) -> CrecimientoTemperatura:
        all_updates = data.as_builtins()
        updates = {k: v for k, v in all_updates.items() if v is not None}
        updated_crecimiento, _ = crecimiento_temperatura_repo.get_and_update(
            match_fields=["id"],
            id=crecimiento_temperatura_id,
            **updates,
            auto_commit=True,
        )
        return updated_crecimiento
    @get("/list-crecimiento_temperatura")
    async def list_crecimiento_temperatura(self,crecimiento_temperatura_repo: CrecimientoTemperaturaRepository,request: Request) -> list[CrecimientoTemperatura]:   
        # 1. Leer todos los query params
        raw_filters: dict[str, Any] = dict(request.query_params)

        # 2. (Opcional) quedarnos sólo con los campos válidos del modelo
        valid_fields = set(CrecimientoTemperatura.__table__.columns.keys())
        filtros = {
            k: v
            for k, v in raw_filters.items()
            if k in valid_fields
        }

        # 3. Llamar al repositorio
        return crecimiento_temperatura_repo.find_many(
            match_fields=list(filtros.keys()),
            **filtros
        )
class ResistenciaAntibioticaController(Controller):
    path = "/resistencia_antibiotica"
    tags = ["ResistenciaAntibiotica"]
    dto = ResistenciaAntibioticaReadDTO
    dependencies = {
        "resistencia_antibiotica_repo": Provide(provide_resistencia_antibiotica_repo),
    }
    
    @get("/get-all")
    async def get_all(self, resistencia_antibiotica_repo: ResistenciaAntibioticaRepository) -> Sequence[ResistenciaAntibiotica]:
        """
        Devuelve todas las instancias de ResistenciaAntibiotica.
        Gracias a `dto = ResistenciaAntibioticaReadDTO`, Litestar convierte cada entidad
        a su DTO correspondiente y luego serializa a JSON.
        """
        return resistencia_antibiotica_repo.list()
    @post("/create", dto=ResistenciaAntibioticaCreateDTO) #CREATE
    async def add_resistencia(self,resistencia_antibiotica_repo: ResistenciaAntibioticaRepository,data: ResistenciaAntibiotica) -> Sequence[ResistenciaAntibiotica]:
        nueva = resistencia_antibiotica_repo.add(data, auto_commit=True)
        return [nueva]
    @patch("/{resistencia_antibiotica_id:int}", dto=ResistenciaAntibioticaUpdateDTO)
    async def update_resistencia(self,resistencia_antibiotica_repo: ResistenciaAntibioticaRepository,resistencia_antibiotica_id: int,data: DTOData[ResistenciaAntibiotica],) -> ResistenciaAntibiotica:
        all_updates = data.as_builtins()
        updates = {k: v for k, v in all_updates.items() if v is not None}
        updated_resistencia, _ = resistencia_antibiotica_repo.get_and_update(
            match_fields=["id"],
            id=resistencia_antibiotica_id,
            **updates,
            auto_commit=True,
        )
        return updated_resistencia
    @get("/list-resistencia_antibiotica")
    async def list_resistencia_antibiotica(self,resistencia_antibiotica_repo: ResistenciaAntibioticaRepository,request: Request) -> list[ResistenciaAntibiotica]:
        # 1. Leer todos los query params
        raw_filters: dict[str, Any] = dict(request.query_params)

        # 2. (Opcional) quedarnos sólo con los campos válidos del modelo
        valid_fields = set(ResistenciaAntibiotica.__table__.columns.keys())
        filtros = {
            k: v
            for k, v in raw_filters.items()
            if k in valid_fields
        }

        # 3. Llamar al repositorio
        return resistencia_antibiotica_repo.find_many(
            match_fields=list(filtros.keys()),
            **filtros
        )
class CaracterizacionGeneticaController(Controller):
    path = "/caracterizacion_genetica"
    tags = ["CaracterizacionGenetica"]
    dto = CaracterizacionGeneticaReadDTO
    dependencies = {
        "caracterizacion_genetica_repo": Provide(provide_caracterizacion_genetica_repo),
    }
    
    @get("/get-all")
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
    @patch("/{caracterizacion_genetica_id:int}", dto=CaracterizacionGeneticaUpdateDTO)
    async def update_caracterizacion(self,caracterizacion_genetica_repo: CaracterizacionGeneticaRepository,caracterizacion_genetica_id: int,data: DTOData[CaracterizacionGenetica],) -> CaracterizacionGenetica:
        all_updates = data.as_builtins()
        updates = {k: v for k, v in all_updates.items() if v is not None}
        updated_caracterizacion, _ = caracterizacion_genetica_repo.get_and_update(
            match_fields=["id"],
            id=caracterizacion_genetica_id,
            **updates,
            auto_commit=True,
        )
        return updated_caracterizacion
    @get("/list-caracterizacion_genetica")
    async def list_caracterizacion_genetica(self,caracterizacion_genetica_repo: CaracterizacionGeneticaRepository,request: Request) -> list[CaracterizacionGenetica]:
        # 1. Leer todos los query params
        raw_filters: dict[str, Any] = dict(request.query_params)

        # 2. (Opcional) quedarnos sólo con los campos válidos del modelo
        valid_fields = set(CaracterizacionGenetica.__table__.columns.keys())
        filtros = {
            k: v
            for k, v in raw_filters.items()
            if k in valid_fields
        }

        # 3. Llamar al repositorio
        return caracterizacion_genetica_repo.find_many(
            match_fields=list(filtros.keys()),
            **filtros
        )
class ProyectoController(Controller):
    path = "/proyectos"
    tags = ["Proyecto"]
    dto = ProyectoReadDTO
    dependencies = {
        "proyecto_repo": Provide(provide_proyecto_repo),
    }
    
    @get("/get-all")
    async def get_all(self, proyecto_repo: ProyectoRepository) -> Sequence[Proyecto]:
        """
        Devuelve todas las instancias de Proyecto.
        Gracias a `dto = ProyectoReadDTO`, Litestar convierte cada entidad
        a su DTO correspondiente y luego serializa a JSON.
        """
        return proyecto_repo.list()
    @post("/create", dto=ProyectoCreateDTO) #CREATE
    async def add_proyecto(self,proyecto_repo: ProyectoRepository,data: Proyecto) -> Sequence[Proyecto]:
        nueva = proyecto_repo.add(data, auto_commit=True)
        return [nueva]
    @patch("/{proyecto_id:int}", dto=ProyectoUpdateDTO)
    async def update_proyecto(self,proyecto_repo: ProyectoRepository,proyecto_id: int,data: DTOData[Proyecto],) -> Proyecto:
        all_updates = data.as_builtins()
        updates = {k: v for k, v in all_updates.items() if v is not None}
        updated_proyecto, _ = proyecto_repo.get_and_update(
            match_fields=["id"],
            id=proyecto_id,
            **updates,
            auto_commit=True,
        )
        return updated_proyecto
    @get("/list-proyecto")
    async def list_proyectos(self,proyecto_repo: ProyectoRepository,request: Request) -> list[Proyecto]:
        # 1. Leer todos los query params
        raw_filters: dict[str, Any] = dict(request.query_params)

        # 2. (Opcional) quedarnos sólo con los campos válidos del modelo
        valid_fields = set(Proyecto.__table__.columns.keys())
        filtros = {
            k: v
            for k, v in raw_filters.items()
            if k in valid_fields
        }

        # 3. Llamar al repositorio
        return proyecto_repo.find_many(
            match_fields=list(filtros.keys()),
            **filtros
        )
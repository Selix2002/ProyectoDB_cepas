from typing import Sequence,Any, Union
from typing import Any
from litestar import Controller, get, post, patch, delete
from litestar.exceptions import HTTPException
from advanced_alchemy.exceptions import NotFoundError
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeMeta
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


    CepaReadDTO,
    CepaUpdateDTO,
    CepaCreateDTO,
    CepaFullReadDTO
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
    async def get_all(self, cepa_repo: CepaRepository = Provide(provide_cepa_repo)) -> list[dict[str, Any]]:
        # 1) Recupero todas las Cepa
        cepas: Sequence[Cepa] = cepa_repo.list()

        # 2) Función recursiva para filtrar columnas "*id" y relaciones "cepa"
        def filter_ids(obj: Any) -> Union[dict[str, Any], list, Any]:
            # Si es lista, aplico recursividad a cada elemento
            if isinstance(obj, list):
                return [filter_ids(item) for item in obj]

            # Si no es un objeto mapeado por SQLAlchemy, lo devuelvo tal cual
            cls = obj.__class__
            if not hasattr(cls, "__mapper__"):
                return obj

            result: dict[str, Any] = {}

            # 2.1) Columnas simples: tomo cada columna mapeada y omito las que terminen en "id"
            for column in cls.__mapper__.columns:
                col_name = column.key
                # Si el nombre de la columna termina en "id" (e.g., "id", "cepa_id"), la salto
                if col_name.endswith("id"):
                    continue
                result[col_name] = getattr(obj, col_name)

            # 2.2) Relaciones: recorro cada relación definida
            for rel in cls.__mapper__.relationships:
                rel_name = rel.key

                # ---------- Punto clave: si la relación apunta de vuelta a Cepa, la salto ----------
                # Normalmente esa relación de backref se llama "cepa". 
                # Si cambiaste el nombre de la relación inversa, pon ahí ese nombre.
                if rel_name == "cepa":
                    continue

                related_obj = getattr(obj, rel_name)

                if related_obj is None:
                    result[rel_name] = None
                else:
                    # Si la relación es 1-a-muchos (lista), aplico recursividad a cada elemento
                    if isinstance(related_obj, list):
                        result[rel_name] = [filter_ids(item) for item in related_obj]
                    else:
                        # Relación 1-a-1 o nulo
                        result[rel_name] = filter_ids(related_obj)

            return result

        # 3) Aplico el filtrado a cada Cepa y retorno la lista de diccionarios
        return [filter_ids(cepa) for cepa in cepas]
    @get("/get-by-id/{id:int}", dto=CepaReadDTO)  # READ
    async def get_by_id(self, id: int, cepa_repo: CepaRepository) -> Cepa:
        try:
            return cepa_repo.get(id)
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Cepa not found")
    @post("/create", dto=CepaCreateDTO) #CREATE
    async def add_cepa(self,cepa_repo: CepaRepository,data: Cepa) -> Sequence[Cepa]:
        
        nueva = cepa_repo.add(data, auto_commit=True)
        return [nueva]
        
    @patch("/update/{cepa_id:int}", dto=CepaUpdateDTO)  # UPDATE
    async def update(self, cepa_id: int, data: DTOData[Cepa], cepa_repo: CepaRepository) -> Cepa:
        try:
        # Extraer el diccionario con los campos que vienen en el DTO
            valores = data.as_builtins()
        # Evitar que 'id' venga dentro de los valores a actualizar
            valores.pop("id", None)

        # Ahora sí llamamos a get_and_update sin que haya colisión de 'id'
            cepa, _ = cepa_repo.get_and_update(
            match_fields=["id"],     # ó "id"
            id=cepa_id,
            **valores,
            auto_commit=True
            )
            return cepa
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Cepa not found")

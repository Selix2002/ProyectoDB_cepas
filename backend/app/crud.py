import string
from typing import Sequence,Any, Union
from typing import Any
from litestar import Controller, get, post, patch, delete,Request
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
    CepaFullReadDTO,
    CepaUpdateJSONBDTO
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

            # 2.1) Columnas simples: tomo cada columna mapeada y omito las que terminen en "id",
            #       salvo que sea la PK "id" de la propia Cepa
            for column in cls.__mapper__.columns:
                col_name = column.key

                # Si termina en "id":
                if col_name.endswith("id"):
                    # --- Permitimos "id" únicamente para la clase Cepa ---
                    if col_name == "id" and isinstance(obj, Cepa):
                        # incluimos cepa.id
                        result[col_name] = getattr(obj, col_name)
                        continue
                    # Para cualquier otro "id" (ej. "cepa_id", o "id" de otras tablas), lo saltamos
                    continue

                # columnas que no terminan en "id"
                result[col_name] = getattr(obj, col_name)

            # 2.2) Relaciones: recorro cada relación definida
            for rel in cls.__mapper__.relationships:
                rel_name = rel.key

                # Si la relación apunta de vuelta a Cepa, la salto (backref)
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
    async def update(self, cepa_id: int, data: DTOData[Cepa], cepa_repo: CepaRepository,request: Request,) -> Cepa:
        try:
            # 1. Obtenemos la instancia de la Cepa que vamos a actualizar.
            #    Usamos .get() en lugar de .get_and_update() por ahora.
            cepa_a_actualizar = cepa_repo.get(cepa_id)
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Cepa not found")

        # 2. Obtener el diccionario directamente de la solicitud, NO del DTO.
        update_data = await request.json()

        # 3. Iteramos sobre los datos recibidos para actualizar el objeto Cepa y sus relaciones.
        for key, value in update_data.items():
            if isinstance(value, dict):
                # Si el valor es un diccionario, es una relación anidada (ej. "almacenamiento").
                related_obj = getattr(cepa_a_actualizar, key, None)
                if related_obj:
                    # Si el objeto relacionado existe (ej. cepa.almacenamiento no es None),
                    # actualizamos sus atributos uno por uno.
                    for     sub_key, sub_value in value.items():
                        setattr(related_obj, sub_key, sub_value)
            # else:
                # Opcional: si la relación no existiera, aquí podrías crearla.
                # Por ejemplo:
                # from app.models import Almacenamiento
                # nuevo_almacenamiento = Almacenamiento(**value)
                # cepa_a_actualizar.almacenamiento = nuevo_almacenamiento
            else:
                print("XDDDDDDDDD",type(value))
                # Si no es un diccionario, es un atributo simple de Cepa (ej. "nombre").
                setattr(cepa_a_actualizar, key, value)

    # 4. Añadimos el objeto modificado a la sesión y hacemos commit.
    #    SQLAlchemy detectará los cambios y generará las sentencias UPDATE correctas.
        cepa_repo.session.add(cepa_a_actualizar)
        cepa_repo.session.commit()
        cepa_repo.session.refresh(cepa_a_actualizar) # Refrescamos para obtener los datos actualizados de la DB.

        return cepa_a_actualizar


    @patch("/update-jsonb/{cepa_name:str}", dto=CepaUpdateJSONBDTO)
    async def update_jsonb(
        self,
        cepa_name: str,
        data: DTOData[Cepa],
        cepa_repo: CepaRepository = Provide(provide_cepa_repo),
    ) -> Cepa:
        try:
            # 1) Extraer sólo el parche para datos_extra
            patch_data = data.as_builtins().get("datos_extra", {})
            
            # 2) Obtener la cepa actual y su JSONB existente
            cepa_actual = cepa_repo.get_and_update(  # o cepa_repo.get(...)
                match_fields=["nombre"],
                nombre=cepa_name,
                auto_commit=False,  # sólo lectura por ahora
            )[0]
            existing_json = cepa_actual.datos_extra or {}

            # 3) Fusionar los dos diccionarios (merge)
            merged_json = {**existing_json, **patch_data}

            # 4) Aplicar el update con el JSON combinado
            updated_cepa, _ = cepa_repo.get_and_update(
                match_fields=["nombre"],
                nombre=cepa_name,
                datos_extra=merged_json,
                auto_commit=True,
            )
            return updated_cepa

        except NotFoundError:
            raise HTTPException(status_code=404, detail="Cepa not found")
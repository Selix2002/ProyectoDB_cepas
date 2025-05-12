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
    ProyectoReadDTO
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
    return_dto=CepaReadDTO
    dependencies = {
        "cepa_repo": Provide(provide_cepa_repo),
    }
from typing import Optional, List

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Clase base para todos los modelos, usando el nuevo estilo DeclarativeBase."""
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=True)

    #Relaciones uno-a-muchos con Cepa

class Cepa(Base):
    __tablename__ = "cepas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    cod_lab: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    pigmentacion: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    origen: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    datos_extra: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    almacenamiento: Mapped[Optional["Almacenamiento"]] = relationship(
        back_populates="cepa",uselist=False
    )
    medio_cultivo: Mapped[Optional["MedioCultivo"]] = relationship(
        back_populates="cepa", uselist=False
    )
    morfologia: Mapped[Optional["Morfologia"]] = relationship(
        back_populates="cepa", uselist=False
    )
    actividad_enzimatica: Mapped[Optional["ActividadEnzimatica"]] = relationship(
        back_populates="cepa", uselist=False
    )
    crecimiento_temperatura: Mapped[Optional["CrecimientoTemperatura"]] = relationship(
        back_populates="cepa", uselist=False
    )
    resistencia_antibiotica: Mapped[Optional["ResistenciaAntibiotica"]] = relationship(
        back_populates="cepa", uselist=False
    )
    caracterizacion_genetica: Mapped[Optional["CaracterizacionGenetica"]] = relationship(
        back_populates="cepa", uselist=False
    )
    proyecto: Mapped[Optional["Proyecto"]] = relationship(
        back_populates="cepa", uselist=False
    )


class Almacenamiento(Base):
    __tablename__ = "almacenamiento"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    envio_puq: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    temperatura_menos80: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cepa_id: Mapped[int] = mapped_column(Integer, ForeignKey("cepas.id"))

    cepa: Mapped["Cepa"] = relationship(back_populates="almacenamiento")


class MedioCultivo(Base):
    __tablename__ = "medios_cultivo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    medio: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cepa_id: Mapped[int] = mapped_column(Integer, ForeignKey("cepas.id"))

    cepa: Mapped["Cepa"] = relationship(back_populates="medio_cultivo")


class Morfologia(Base):
    __tablename__ = "morfologia"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gram: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    morfologia_1: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    morfologia_2: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cepa_id: Mapped[int] = mapped_column(Integer, ForeignKey("cepas.id"))

    cepa: Mapped["Cepa"] = relationship(back_populates="morfologia")


class ActividadEnzimatica(Base):
    __tablename__ = "actividad_enzimatica"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lecitinasa: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ureasa: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    lipasa: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    amilasa: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    proteasa: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    catalasa: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    celulasa: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fosfatasa: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    aia: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cepa_id: Mapped[int] = mapped_column(Integer, ForeignKey("cepas.id"))

    cepa: Mapped["Cepa"] = relationship(back_populates="actividad_enzimatica")


class CrecimientoTemperatura(Base):
    __tablename__ = "crecimiento_temperatura"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    temp_5: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    temp_25: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    temp_37: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cepa_id: Mapped[int] = mapped_column(Integer, ForeignKey("cepas.id"))

    cepa: Mapped["Cepa"] = relationship(back_populates="crecimiento_temperatura")


class ResistenciaAntibiotica(Base):
    __tablename__ = "resistencia_antibiotica"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amp: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ctx: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cxm: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    caz: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ak: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    c: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    te: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    am_ecoli: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    am_saureus: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cepa_id: Mapped[int] = mapped_column(Integer, ForeignKey("cepas.id"))

    cepa: Mapped["Cepa"] = relationship(back_populates="resistencia_antibiotica")


class CaracterizacionGenetica(Base):
    __tablename__ = "caracterizacion_genetica"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gen_16s: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    metabolomica: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cepa_id: Mapped[int] = mapped_column(Integer, ForeignKey("cepas.id"))

    cepa: Mapped["Cepa"] = relationship(back_populates="caracterizacion_genetica")


class Proyecto(Base):
    __tablename__ = "proyectos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    responsable: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    nombre_proyecto: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cepa_id: Mapped[int] = mapped_column(Integer, ForeignKey("cepas.id"))

    cepa: Mapped["Cepa"] = relationship(back_populates="proyecto")

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()

class Cepa(Base):
    __tablename__ = 'cepas'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    cod_lab = Column(String, nullable=True)
    pigmentacion = Column(String, nullable=True)
    origen = Column(String, nullable=True)
    datos_extra = Column(JSONB, nullable=True)  # Campo flexible tipo JSONB

    almacenamiento = relationship("Almacenamiento", back_populates="cepa", uselist=False)
    medio_cultivo = relationship("MedioCultivo", back_populates="cepa", uselist=False)
    morfologia = relationship("Morfologia", back_populates="cepa", uselist=False)
    actividad_enzimatica = relationship("ActividadEnzimatica", back_populates="cepa", uselist=False)
    crecimiento_temperatura = relationship("CrecimientoTemperatura", back_populates="cepa", uselist=False)
    resistencia_antibiotica = relationship("ResistenciaAntibiotica", back_populates="cepa", uselist=False)
    caracterizacion_genetica = relationship("CaracterizacionGenetica", back_populates="cepa", uselist=False)
    proyecto = relationship("Proyecto", back_populates="cepa", uselist=False)

class Almacenamiento(Base):
    __tablename__ = 'almacenamiento'

    id = Column(Integer, primary_key=True)
    envio_puq = Column(String, nullable=True)
    temperatura_menos80 = Column(String, nullable=True)
    cepa_id = Column(Integer, ForeignKey('cepas.id'))
    cepa = relationship("Cepa", back_populates="almacenamiento")

class MedioCultivo(Base):
    __tablename__ = 'medios_cultivo'

    id = Column(Integer, primary_key=True)
    medio = Column(String, nullable=True)
    cepa_id = Column(Integer, ForeignKey('cepas.id'))
    cepa = relationship("Cepa", back_populates="medio_cultivo")

class Morfologia(Base):
    __tablename__ = 'morfologia'

    id = Column(Integer, primary_key=True)
    gram = Column(String, nullable=True)
    morfologia_1 = Column(String, nullable=True)
    morfologia_2 = Column(String, nullable=True)
    cepa_id = Column(Integer, ForeignKey('cepas.id'))
    cepa = relationship("Cepa", back_populates="morfologia")

class ActividadEnzimatica(Base):
    __tablename__ = 'actividad_enzimatica'

    id = Column(Integer, primary_key=True)
    lecitinasa = Column(String, nullable=True)
    ureasa = Column(String, nullable=True)
    lipasa = Column(String, nullable=True)
    amilasa = Column(String, nullable=True)
    proteasa = Column(String, nullable=True)
    catalasa = Column(String, nullable=True)
    celulasa = Column(String, nullable=True)
    fosfatasa = Column(String, nullable=True)
    aia = Column(String, nullable=True)
    cepa_id = Column(Integer, ForeignKey('cepas.id'))
    cepa = relationship("Cepa", back_populates="actividad_enzimatica")

class CrecimientoTemperatura(Base):
    __tablename__ = 'crecimiento_temperatura'

    id = Column(Integer, primary_key=True)
    temp_5 = Column(String, nullable=True)
    temp_25 = Column(String, nullable=True)
    temp_37 = Column(String, nullable=True)
    cepa_id = Column(Integer, ForeignKey('cepas.id'))
    cepa = relationship("Cepa", back_populates="crecimiento_temperatura")

class ResistenciaAntibiotica(Base):
    __tablename__ = 'resistencia_antibiotica'

    id = Column(Integer, primary_key=True)
    amp = Column(String, nullable=True)
    ctx = Column(String, nullable=True)
    cxm = Column(String, nullable=True)
    caz = Column(String, nullable=True)
    ak = Column(String, nullable=True)
    c = Column(String, nullable=True)
    te = Column(String, nullable=True)
    am_ecoli = Column(String, nullable=True)
    am_saureus = Column(String, nullable=True)
    cepa_id = Column(Integer, ForeignKey('cepas.id'))
    cepa = relationship("Cepa", back_populates="resistencia_antibiotica")

class CaracterizacionGenetica(Base):
    __tablename__ = 'caracterizacion_genetica'

    id = Column(Integer, primary_key=True)
    gen_16s = Column(String, nullable=True)
    metabolomica = Column(String, nullable=True)
    cepa_id = Column(Integer, ForeignKey('cepas.id'))
    cepa = relationship("Cepa", back_populates="caracterizacion_genetica")

class Proyecto(Base):
    __tablename__ = 'proyectos'

    id = Column(Integer, primary_key=True)
    responsable = Column(String, nullable=True)
    nombre_proyecto = Column(String, nullable=True)
    cepa_id = Column(Integer, ForeignKey('cepas.id'))
    cepa = relationship("Cepa", back_populates="proyecto")

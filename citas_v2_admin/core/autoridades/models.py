"""
Autoridades, modelos
"""
from collections import OrderedDict
from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Autoridad(Base, UniversalMixin):
    """Autoridad"""

    ORGANOS_JURISDICCIONALES = OrderedDict(
        [
            ("NO DEFINIDO", "No Definido"),
            ("JUZGADO DE PRIMERA INSTANCIA", "Juzgado de Primera Instancia"),
            ("JUZGADO DE PRIMERA INSTANCIA ORAL", "Juzgado de Primera Instancia Oral"),
            ("PLENO O SALA DEL TSJ", "Pleno o Sala del TSJ"),
            ("TRIBUNAL DISTRITAL", "Tribunal Distrital"),
            ("TRIBUNAL DE CONCILIACION Y ARBITRAJE", "Tribunal de Conciliación y Arbitraje"),
        ]
    )

    # Nombre de la tabla
    __tablename__ = "autoridades"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foráneas
    distrito_id = Column(Integer, ForeignKey("distritos.id"), index=True, nullable=False)
    distrito = relationship("Distrito", back_populates="autoridades")
    materia_id = Column(Integer, ForeignKey("materias.id"), index=True, nullable=False)
    materia = relationship("Materia", back_populates="autoridades")

    # Columnas
    clave = Column(String(16), nullable=False, unique=True)
    descripcion = Column(String(256), nullable=False)
    descripcion_corta = Column(String(64), nullable=False)
    es_jurisdiccional = Column(Boolean(), nullable=False, default=False)
    es_notaria = Column(Boolean(), nullable=False, default=False)
    es_organo_especializado = Column(Boolean(), nullable=False, default=False)
    organo_jurisdiccional = Column(
        Enum(*ORGANOS_JURISDICCIONALES, name="tipos_organos_jurisdiccionales", native_enum=False),
        index=True,
        nullable=False,
    )

    # Hijos
    usuarios = relationship("Usuario", back_populates="autoridad")

    @property
    def es_creador_glosas(self):
        """Es creador de glosas"""
        return self.organo_jurisdiccional in ["PLENO O SALA DEL TSJ", "TRIBUNAL DE CONCILIACION Y ARBITRAJE"]

    @property
    def distrito_clave(self):
        """Clave del distrito"""
        return self.distrito.clave

    @property
    def distrito_nombre(self):
        """Nombre del distrito"""
        return self.distrito.nombre

    @property
    def distrito_nombre_corto(self):
        """Nombre corto del distrito"""
        return self.distrito.nombre_corto

    @property
    def materia_clave(self):
        """Clave de la materia"""
        return self.materia.clave

    @property
    def materia_nombre(self):
        """Nombre de la materia"""
        return self.materia.nombre

    def __repr__(self):
        """Representación"""
        return f"<Autoridad {self.id}>"

"""
Cit Categorias, modelos
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class CitCategoria(Base, UniversalMixin):
    """CitCategoria"""

    # Nombre de la tabla
    __tablename__ = "cit_categorias"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Columnas
    nombre: Mapped[str] = mapped_column(String(64), unique=True)

    # Hijos
    cit_servicios: Mapped["CitServicio"] = relationship("CitServicio", back_populates="cit_categoria")

    def __repr__(self):
        """Representación"""
        return f"<CitCategoria {self.nombre}>"

"""
Cit Horas Bloqueadas, modelos
"""

from datetime import date, time

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class CitHoraBloqueada(Base, UniversalMixin):
    """CitHoraBloqueada"""

    # Nombre de la tabla
    __tablename__ = "cit_horas_bloqueadas"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Clave foránea
    oficina_id: Mapped[int] = mapped_column(ForeignKey("oficinas.id"), index=True)
    oficina: Mapped["Oficina"] = relationship(back_populates="cit_horas_bloqueadas")

    # Columnas
    fecha: Mapped[date] = mapped_column(index=True)
    inicio: Mapped[time]
    termino: Mapped[time]
    descripcion: Mapped[str] = mapped_column(String(256))

    @property
    def oficina_clave(self):
        """Clave de la oficina"""
        return self.oficina.clave

    @property
    def oficina_descripcion(self):
        """Descripcion de la oficina"""
        return self.oficina.descripcion

    @property
    def oficina_descripcion_corta(self):
        """Descripcion corta de la oficina"""
        return self.oficina.descripcion_corta

    def __repr__(self):
        """Representación"""
        return f"<CitHoraBloqueada {self.id}>"

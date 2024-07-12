"""
Cit Oficinas Servicios, modelos
"""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class CitOficinaServicio(Base, UniversalMixin):
    """CitOficinaServicio"""

    # Nombre de la tabla
    __tablename__ = "cit_oficinas_servicios"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Claves foráneas
    cit_servicio_id: Mapped[int] = mapped_column(ForeignKey("cit_servicios.id"), index=True)
    cit_servicio: Mapped["CitServicio"] = relationship(back_populates="cit_oficinas_servicios")
    oficina_id: Mapped[int] = mapped_column(ForeignKey("oficinas.id"), index=True)
    oficina: Mapped["Oficina"] = relationship(back_populates="cit_oficinas_servicios")

    # Columnas
    descripcion: Mapped[str] = mapped_column(String(256))

    @property
    def cit_servicio_clave(self):
        """Clave del servicio"""
        return self.cit_servicio.clave

    @property
    def cit_servicio_descripcion(self):
        """Descripcion del servicio"""
        return self.cit_servicio.descripcion

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
        return f"<CitOficinaServicio {self.id}>"

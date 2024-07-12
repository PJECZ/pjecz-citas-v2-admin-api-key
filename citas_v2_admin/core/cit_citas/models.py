"""
Cit Citas, modelos
"""

from datetime import datetime

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class CitCita(Base, UniversalMixin):
    """CitCita"""

    ESTADOS = {
        "ASISTIO": "Asistió",
        "CANCELO": "Canceló",
        "INASISTENCIA": "Inasistencia",
        "PENDIENTE": "Pendiente",
    }

    # Nombre de la tabla
    __tablename__ = "cit_citas"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Claves foráneas
    cit_cliente_id: Mapped[int] = mapped_column(ForeignKey("cit_clientes.id"), index=True)
    cit_cliente: Mapped["CitCliente"] = relationship(back_populates="cit_citas")
    cit_servicio_id: Mapped[int] = mapped_column(ForeignKey("cit_servicios.id"), index=True)
    cit_servicio: Mapped["CitServicio"] = relationship(back_populates="cit_citas")
    oficina_id: Mapped[int] = mapped_column(ForeignKey("oficinas.id"), index=True)
    oficina: Mapped["Oficina"] = relationship(back_populates="cit_citas")

    # Columnas
    inicio: Mapped[datetime]
    termino: Mapped[datetime]
    notas: Mapped[str] = mapped_column(Text())
    estado: Mapped[str] = mapped_column(Enum(*ESTADOS, name="estados", native_enum=False), index=True)
    asistencia: Mapped[bool] = mapped_column(default=False)
    codigo_asistencia: Mapped[str] = mapped_column(String(4))
    cancelar_antes: Mapped[datetime]

    @property
    def cit_cliente_nombre(self):
        """Nombre del cliente"""
        return self.cit_cliente.nombre

    @property
    def cit_cliente_curp(self):
        """Curp del cliente"""
        return self.cit_cliente.curp

    @property
    def cit_cliente_email(self):
        """Email del cliente"""
        return self.cit_cliente.email

    @property
    def cit_servicio_clave(self):
        """Clave del servicio"""
        return self.cit_servicio.clave

    @property
    def cit_servicio_descripcion(self):
        """Descripción del servicio"""
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
        return f"<CitCita {self.id}>"

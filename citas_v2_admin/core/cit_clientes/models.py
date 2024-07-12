"""
Cit Clientes, modelos
"""

from datetime import date
from typing import List

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class CitCliente(Base, UniversalMixin):
    """CitCliente"""

    # Nombre de la tabla
    __tablename__ = "cit_clientes"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Columnas
    nombres: Mapped[str] = mapped_column(String(256))
    apellido_primero: Mapped[str] = mapped_column(String(256))
    apellido_segundo: Mapped[str] = mapped_column(String(256))
    curp: Mapped[str] = mapped_column(String(18), unique=True)
    telefono: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(256), unique=True)
    contrasena_md5: Mapped[str] = mapped_column(String(256))
    contrasena_sha256: Mapped[str] = mapped_column(String(256))
    renovacion: Mapped[date]
    limite_citas_pendientes: Mapped[int] = mapped_column(default=0)

    # Columnas booleanas
    autoriza_mensajes: Mapped[bool] = mapped_column(default=True)
    enviar_boletin: Mapped[bool] = mapped_column(default=False)
    es_adulto_mayor: Mapped[bool] = mapped_column(default=False)
    es_mujer: Mapped[bool] = mapped_column(default=False)
    es_identidad: Mapped[bool] = mapped_column(default=False)
    es_discapacidad: Mapped[bool] = mapped_column(default=False)
    es_personal_interno: Mapped[bool] = mapped_column(default=False)

    # Hijos
    cit_citas: Mapped[List["CitCita"]] = relationship("CitCita", back_populates="cit_cliente")
    cit_clientes_recuperaciones: Mapped[List["CitClienteRecuperacion"]] = relationship(
        "CitClienteRecuperacion", back_populates="cit_cliente"
    )

    @property
    def nombre(self):
        """Junta nombres, apellido_primero y apellido segundo"""
        return self.nombres + " " + self.apellido_primero + " " + self.apellido_segundo

    def __repr__(self):
        """Representación"""
        return f"<CitCliente {self.email}>"

"""
Cit Clientes Registros, modelos
"""

from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class CitClienteRegistro(Base, UniversalMixin):
    """CitClienteRegistro"""

    # Nombre de la tabla
    __tablename__ = "cit_clientes_registros"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Columnas
    nombres: Mapped[str] = mapped_column(String(256))
    apellido_primero: Mapped[str] = mapped_column(String(256))
    apellido_segundo: Mapped[str] = mapped_column(String(256))
    curp: Mapped[str] = mapped_column(String(18), index=True)
    telefono: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(256), index=True)
    expiracion: Mapped[datetime]
    cadena_validar: Mapped[str] = mapped_column(String(256))
    mensajes_cantidad: Mapped[int] = mapped_column(default=0)
    ya_registrado: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        """Representación"""
        return f"<CitClienteRegistro {self.id}>"

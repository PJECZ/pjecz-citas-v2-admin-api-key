"""
Boletines, modelos
"""

from datetime import datetime

from sqlalchemy import JSON, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Boletin(Base, UniversalMixin):
    """Boletin"""

    ESTADOS = {
        "BORRADOR": "Borrador",
        "PROGRAMADO": "Programado",
        "ENVIADO": "Enviado",
    }

    # Nombre de la tabla
    __tablename__ = "boletines"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Columnas
    asunto: Mapped[str] = mapped_column(String(256))
    contenido: Mapped[dict] = mapped_column(JSON())
    estado: Mapped[str] = mapped_column(Enum(*ESTADOS, name="boletines_estados", native_enum=False), index=True)
    envio_programado: Mapped[datetime]
    puntero: Mapped[int] = mapped_column(Integer, default=0)
    termino_programado: Mapped[datetime]

    def __repr__(self):
        """Representación"""
        return f"<Boletin {self.id}>"

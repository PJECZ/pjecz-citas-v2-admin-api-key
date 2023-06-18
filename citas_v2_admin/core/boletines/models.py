"""
Boletines, modelos
"""
from collections import OrderedDict

from sqlalchemy import Column, DateTime, Enum, JSON, Integer, String

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Boletin(Base, UniversalMixin):
    """Boletin"""

    ESTADOS = OrderedDict(
        [
            ("BORRADOR", "Borrador"),
            ("PROGRAMADO", "Programado"),
            ("ENVIADO", "Enviado"),
        ]
    )

    # Nombre de la tabla
    __tablename__ = "boletines"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    asunto = Column(String(256), nullable=False)
    contenido = Column(JSON())
    estado = Column(
        Enum(*ESTADOS, name="boletines_estados", native_enum=False),
        index=True,
        nullable=False,
    )
    envio_programado = Column(DateTime(), nullable=False)
    puntero = Column(Integer, nullable=False, default=0)
    termino_programado = Column(DateTime(), nullable=False)

    def __repr__(self):
        """Representación"""
        return f"<Boletin {self.id}>"

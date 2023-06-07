"""
Bitacoras v3, esquemas de pydantic
"""
from datetime import datetime

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class BitacoraOut(BaseModel):
    """Esquema para entregar bitacoras"""

    id: int | None
    modulo_id: int | None
    modulo_nombre: str | None
    usuario_id: int | None
    usuario_nombre: str | None
    descripcion: str | None
    url: str | None
    creado: datetime | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneBitacoraOut(BitacoraOut, OneBaseOut):
    """Esquema para entregar una bitacora"""

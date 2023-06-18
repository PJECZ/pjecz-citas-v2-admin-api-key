"""
Boletines v3, esquemas de pydantic
"""
from datetime import datetime
from typing import Dict

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class BoletinOut(BaseModel):
    """Esquema para entregar boletines"""

    id: int | None
    asunto: str | None
    contenido: Dict | None
    estado: str | None
    envio_programado: datetime | None
    puntero: int | None
    termino_programado: datetime | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneBoletinOut(BoletinOut, OneBaseOut):
    """Esquema para entregar un boletin"""

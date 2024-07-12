"""
Boletines v4, esquemas de pydantic
"""
from datetime import datetime
from typing import Dict

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class BoletinOut(BaseModel):
    """Esquema para entregar boletines"""

    id: int | None = None
    asunto: str | None = None
    contenido: Dict | None = None
    estado: str | None = None
    envio_programado: datetime | None = None
    puntero: int | None = None
    termino_programado: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


class OneBoletinOut(BoletinOut, OneBaseOut):
    """Esquema para entregar un boletin"""

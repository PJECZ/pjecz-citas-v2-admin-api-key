"""
Cit Dias Inhabiles v4, esquemas de pydantic
"""
from datetime import date

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class CitDiaInhabilIn(BaseModel):
    """Esquema para recibir un dia inhabil"""

    fecha: date
    descripcion: str


class CitDiaInhabilOut(CitDiaInhabilIn):
    """Esquema para entregar dias inhabiles"""

    id: int | None = None
    model_config = ConfigDict(from_attributes=True)


class OneCitDiaInhabilOut(CitDiaInhabilOut, OneBaseOut):
    """Esquema para entregar un dia inhabil"""

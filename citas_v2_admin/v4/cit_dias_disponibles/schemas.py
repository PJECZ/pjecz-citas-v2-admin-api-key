"""
Cit Dias Disponibles v4, esquemas de pydantic
"""
from datetime import date

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitDiasDisponiblesOut(BaseModel):
    """Esquema para entregar dias disponibles"""

    fecha: date


class OneCitDiasDisponiblesOut(CitDiasDisponiblesOut, OneBaseOut):
    """Esquema para entregar un dia disponible"""

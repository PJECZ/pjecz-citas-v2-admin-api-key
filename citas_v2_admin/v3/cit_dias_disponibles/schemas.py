"""
Cit Dias Disponibles v3, esquemas de pydantic
"""
from datetime import date

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitDiaDisponibleOut(BaseModel):
    """Esquema para entregar dias disponibles"""

    fecha: date | None


class OneCitDiaDisponibleOut(CitDiaDisponibleOut, OneBaseOut):
    """Esquema para entregar un dia disponible"""

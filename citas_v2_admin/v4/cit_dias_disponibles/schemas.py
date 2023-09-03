"""
Cit Dias Disponibles v4, esquemas de pydantic
"""
from datetime import date

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitDiaDisponibleOut(BaseModel):
    """Esquema para entregar dias disponibles"""

    fecha: date


class OneCitDiaDisponibleOut(CitDiaDisponibleOut, OneBaseOut):
    """Esquema para entregar un dia disponible"""

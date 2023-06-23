"""
Cit Horas Disponibles v3, esquemas de pydantic
"""
from datetime import time

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitHoraDisponibleOut(BaseModel):
    """Esquema para entregar horas disponibles"""

    horas_minutos: time


class OneCitHoraDisponibleOut(CitHoraDisponibleOut, OneBaseOut):
    """Esquema para entregar una hora disponible"""

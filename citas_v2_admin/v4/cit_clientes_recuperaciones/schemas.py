"""
Cit Clientes Recuperaciones v4, esquemas de pydantic
"""
from datetime import date

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class CitClienteRecuperacionOut(BaseModel):
    """Esquema para entregar recuperaciones"""

    id: int | None = None
    relacion_id: int | None = None
    relacion_nombre: str | None = None
    fecha: date | None = None
    nombre: str | None = None
    descripcion: str | None = None
    archivo: str | None = None
    url: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneCitClienteRecuperacionOut(CitClienteRecuperacionOut, OneBaseOut):
    """Esquema para entregar un recuperacion"""


class CitClientesRecuperacionesCreadosPorDiaOut(BaseModel):
    """Esquema para entregar cantidades de recuperaciones creadas por dia"""

    creado: date | None = None
    cantidad: int | None = None

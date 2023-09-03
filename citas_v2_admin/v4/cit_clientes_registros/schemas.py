"""
Cit Clientes Registros v4, esquemas de pydantic
"""
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class CitClienteRegistroOut(BaseModel):
    """Esquema para entregar registros de clientes"""

    id: int | None = None
    nombres: str | None = None
    apellido_primero: str | None = None
    apellido_segundo: str | None = None
    curp: str | None = None
    telefono: str | None = None
    email: str | None = None
    expiracion: datetime | None = None
    cadena_validar: str | None = None
    mensajes_cantidad: int | None = None
    ya_registrado: bool | None = None
    creado: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


class OneCitClienteRegistroOut(CitClienteRegistroOut, OneBaseOut):
    """Esquema para entregar un regitro de cliente"""


class CitClientesRegistrosCreadosPorDiaOut(BaseModel):
    """Esquema para entregar cantidades de registros creados por dia"""

    creado: date | None = None
    cantidad: int | None = None

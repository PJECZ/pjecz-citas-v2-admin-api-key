"""
Cit Clientes v4, esquemas de pydantic
"""
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class CitClienteOut(BaseModel):
    """Esquema para entregar clientes"""

    id: int | None = None
    nombres: str | None = None
    apellido_primero: str | None = None
    apellido_segundo: str | None = None
    nombre: str | None = None
    curp: str | None = None
    telefono: str | None = None
    email: str | None = None
    contrasena_md5: str | None = None
    contrasena_sha256: str | None = None
    renovacion: date | None = None
    limite_citas_pendientes: int | None = None
    autoriza_mensajes: bool | None = None
    enviar_boletin: bool | None = None
    es_adulto_mayor: bool | None = None
    es_mujer: bool | None = None
    es_identidad: bool | None = None
    es_discapacidad: bool | None = None
    creado: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


class OneCitClienteOut(CitClienteOut, OneBaseOut):
    """Esquema para entregar un cliente"""


class CitClientesCreadosPorDiaOut(BaseModel):
    """Esquema para entregar cantidades de clientes creados por dia"""

    creado: date | None = None
    cantidad: int | None = None

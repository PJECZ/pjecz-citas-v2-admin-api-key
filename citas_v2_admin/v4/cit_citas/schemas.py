"""
Cit Citas v4, esquemas de pydantic
"""
from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class CitCitaCancelIn(BaseModel):
    """Esquema para cancelar una cita"""

    id: int
    cit_cliente_id: int


class CitCitaIn(BaseModel):
    """Esquema para crear una cita"""

    cit_cliente_id: int
    cit_servicio_id: int
    fecha: date
    hora_minuto: time
    oficina_id: int
    notas: str


class CitCitaOut(BaseModel):
    """Esquema para entregar citas"""

    id: int | None = None
    cit_cliente_id: int | None = None
    cit_cliente_nombre: str | None = None
    cit_cliente_curp: str | None = None
    cit_cliente_email: str | None = None
    cit_servicio_id: int | None = None
    cit_servicio_clave: str | None = None
    cit_servicio_descripcion: str | None = None
    oficina_id: int | None = None
    oficina_clave: str | None = None
    oficina_descripcion: str | None = None
    oficina_descripcion_corta: str | None = None
    inicio: datetime | None = None
    termino: datetime | None = None
    notas: str | None = None
    estado: str | None = None
    asistencia: bool | None = None
    codigo_asistencia: str | None = None
    creado: datetime | None = None
    puede_cancelarse: bool | None = None
    model_config = ConfigDict(from_attributes=True)


class OneCitCitaOut(CitCitaOut, OneBaseOut):
    """Esquema para entregar un cita"""


class CitCitasCreadosPorDiaOut(BaseModel):
    """Esquema para entregar cantidades de citas creadas por dia"""

    creado: date | None = None
    cantidad: int | None = None


class CitCitasCreadosPorDiaDistritoOut(BaseModel):
    """Esquema para entregar cantidades de citas creadas por dia"""

    creado: date | None = None
    distrito: str | None = None
    cantidad: int | None = None


class CitCitasAgendadasPorServicioOficinaOut(BaseModel):
    """Esquema para entregar cantidades de citas agendadas por servicio y oficina"""

    oficina: str | None = None
    servicio: str | None = None
    cantidad: int | None = None


class CitCitasDisponiblesCantidadOut(OneBaseOut):
    """Esquema para entregar la cantidad de citas disponibles"""

    cantidad: int | None = None

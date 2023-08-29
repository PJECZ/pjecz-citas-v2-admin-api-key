"""
Cit Horas Bloqueadas v4, esquemas de pydantic
"""
from datetime import date, time

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class CitHoraBloqueadaOut(BaseModel):
    """Esquema para entregar horas bloqueadas"""

    id: int | None = None
    oficina_id: int | None = None
    oficina_clave: str | None = None
    oficina_descripcion: str | None = None
    oficina_descripcion_corta: str | None = None
    fecha: date | None = None
    inicio: time | None = None
    termino: time | None = None
    descripcion: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneCitHoraBloqueadaOut(CitHoraBloqueadaOut, OneBaseOut):
    """Esquema para entregar un hora bloqueada"""

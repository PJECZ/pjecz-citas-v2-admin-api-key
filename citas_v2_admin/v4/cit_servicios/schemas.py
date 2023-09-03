"""
Cit Servicios v4, esquemas de pydantic
"""
from datetime import time

from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class CitServicioOut(BaseModel):
    """Esquema para entregar servicios"""

    id: int | None = None
    cit_categoria_id: int | None = None
    cit_categoria_nombre: str | None = None
    clave: str | None = None
    descripcion: str | None = None
    duracion: time | None = None
    documentos_limite: int | None = None
    desde: time | None = None
    hasta: time | None = None
    dias_habilitados: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneCitServicioOut(CitServicioOut, OneBaseOut):
    """Esquema para entregar un servicio"""

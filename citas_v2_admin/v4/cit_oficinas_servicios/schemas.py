"""
Cit Oficinas Servicios v4, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class CitOficinaServicioOut(BaseModel):
    """Esquema para entregar oficinas-servicios"""

    id: int | None = None
    oficina_id: int | None = None
    oficina_clave: str | None = None
    cit_servicio_id: int | None = None
    cit_servicio_nombre: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneCitOficinaServicioOut(CitOficinaServicioOut, OneBaseOut):
    """Esquema para entregar un oficina-servicio"""

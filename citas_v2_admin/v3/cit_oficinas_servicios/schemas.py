"""
Cit Oficinas-Servicios v3, esquemas de pydantic
"""
from datetime import date

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class CitOficinaServicioOut(BaseModel):
    """Esquema para entregar oficinas-servicios"""

    id: int | None
    relacion_id: int | None
    relacion_nombre: str | None
    fecha: date | None
    nombre: str | None
    descripcion: str | None
    archivo: str | None
    url: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneCitOficinaServicioOut(CitOficinaServicioOut, OneBaseOut):
    """Esquema para entregar un oficina-servicio"""

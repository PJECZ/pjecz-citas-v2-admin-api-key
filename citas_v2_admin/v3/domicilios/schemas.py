"""
Domicilios v3, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class DomicilioOut(BaseModel):
    """Esquema para entregar domicilios"""

    id: int | None
    distrito_id: int | None
    distrito_clave: str | None
    distrito_nombre: str | None
    distrito_nombre_corto: str | None
    edificio: str | None
    estado: str | None
    municipio: str | None
    calle: str | None
    num_ext: str | None
    num_int: str | None
    colonia: str | None
    cp: int | None
    completo: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneDomicilioOut(DomicilioOut, OneBaseOut):
    """Esquema para entregar un domicilio"""

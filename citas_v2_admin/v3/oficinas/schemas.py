"""
Oficinas v3, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class OficinaOut(BaseModel):
    """Esquema para entregar oficinas"""

    id: int | None
    distrito_id: int | None
    distrito_clave: str | None
    distrito_nombre: str | None
    distrito_nombre_corto: str | None
    domicilio_id: int | None
    domicilio_completo: str | None
    domicilio_edificio: str | None
    clave: str | None
    descripcion: str | None
    descripcion_corta: str | None
    es_jurisdiccional: bool | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneOficinaOut(OficinaOut, OneBaseOut):
    """Esquema para entregar un oficina"""

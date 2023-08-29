"""
Cit Categorias v4, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class CitCategoriaOut(BaseModel):
    """Esquema para entregar categorias"""

    id: int | None = None
    nombre: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneCitCategoriaOut(CitCategoriaOut, OneBaseOut):
    """Esquema para entregar una categoria"""

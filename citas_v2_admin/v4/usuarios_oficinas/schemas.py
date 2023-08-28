"""
Usuarios-Oficinas v4, esquemas de pydantic
"""
from pydantic import BaseModel, ConfigDict

from lib.schemas_base import OneBaseOut


class UsuarioOficinaOut(BaseModel):
    """Esquema para entregar usuarios-oficinas"""

    id: int | None = None
    oficina_id: int | None = None
    oficina_nombre: str | None = None
    usuario_id: int | None = None
    usuario_nombre: str | None = None
    descripcion: str | None = None
    model_config = ConfigDict(from_attributes=True)


class OneUsuarioOficinaOut(UsuarioOficinaOut, OneBaseOut):
    """Esquema para entregar un usuario-oficina"""

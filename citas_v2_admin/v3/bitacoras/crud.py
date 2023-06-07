"""
Bitacoras v3, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_email

from ...core.bitacoras.models import Bitacora
from ..usuarios.crud import get_usuario


def get_bitacoras(
    db: Session,
    usuario_id: int = None,
    usuario_email: str = None,
) -> Any:
    """Consultar las bitacoras activas"""
    consulta = db.query(Bitacora)
    if usuario_id is not None:
        usuario = get_usuario(db, usuario_id)
        consulta = consulta.filter(usuario == usuario)
    if usuario_email is not None:
        try:
            usuario_email = safe_email(usuario_email, search_fragment=True)
        except ValueError as error:
            raise MyNotValidParamError("El email no es válido") from error
        consulta = consulta.filter(Bitacora.usuario.email.contains(usuario_email))
    return consulta.filter_by(estatus="A").order_by(Bitacora.id.desc())


def get_bitacora(db: Session, bitacora_id: int) -> Bitacora:
    """Consultar una bitacora por su id"""
    bitacora = db.query(Bitacora).get(bitacora_id)
    if bitacora is None:
        raise MyNotExistsError("No existe ese bitacora")
    if bitacora.estatus != "A":
        raise MyIsDeletedError("No es activo ese bitacora, está eliminado")
    return bitacora

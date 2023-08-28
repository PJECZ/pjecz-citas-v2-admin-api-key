"""
Usuarios-Oficinas v4, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.usuarios_oficinas.models import UsuarioOficina
from ..oficinas.crud import get_oficina, get_oficina_with_clave
from ..usuarios.crud import get_usuario, get_usuario_with_email


def get_usuarios_oficinas(
    database: Session,
    oficina_id: int = None,
    oficina_clave: str = None,
    usuario_id: int = None,
    usuario_email: str = None,
) -> Any:
    """Consultar los usuarios-oficinas activos"""
    consulta = database.query(UsuarioOficina)
    if oficina_id is not None:
        oficina = get_oficina(database, oficina_id)
        consulta = consulta.filter_by(oficina_id=oficina.id)
    elif oficina_clave is not None:
        oficina = get_oficina_with_clave(database, oficina_clave)
        consulta = consulta.filter_by(oficina_id=oficina.id)
    if usuario_id is not None:
        usuario = get_usuario(database, usuario_id)
        consulta = consulta.filter_by(usuario_id=usuario.id)
    elif usuario_email is not None:
        usuario = get_usuario_with_email(database, usuario_email)
        consulta = consulta.filter_by(usuario_id=usuario.id)
    return consulta.filter_by(estatus="A").order_by(UsuarioOficina.id)


def get_usuario_oficina(database: Session, usuario_oficina_id: int) -> UsuarioOficina:
    """Consultar un usuario-oficina por su id"""
    usuario_oficina = database.query(UsuarioOficina).get(usuario_oficina_id)
    if usuario_oficina is None:
        raise MyNotExistsError("No existe ese usuario-oficina")
    if usuario_oficina.estatus != "A":
        raise MyIsDeletedError("No es activo ese usuario-oficina, está eliminado")
    return usuario_oficina

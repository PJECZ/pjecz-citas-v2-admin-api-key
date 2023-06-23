"""
Usuarios-Oficinas v3, rutas (paths)
"""
from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import DatabaseSession
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import CurrentUser

from .crud import get_usuarios_oficinas, get_usuario_oficina
from .schemas import UsuarioOficinaOut, OneUsuarioOficinaOut

usuarios_oficinas = APIRouter(prefix="/v3/usuarios_oficinas", tags=["categoria"])


@usuarios_oficinas.get("", response_model=CustomPage[UsuarioOficinaOut])
async def listado_usuarios_oficinas(
    current_user: CurrentUser,
    db: DatabaseSession,
    oficina_id: int = None,
    usuario_id: int = None,
):
    """Listado de usuarios-oficinas"""
    if current_user.permissions.get("USUARIOS OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_usuarios_oficinas(
            db=db,
            oficina_id=oficina_id,
            usuario_id=usuario_id,
        )
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@usuarios_oficinas.get("/{usuario_oficina_id}", response_model=OneUsuarioOficinaOut)
async def detalle_usuario_oficina_id(
    current_user: CurrentUser,
    db: DatabaseSession,
    usuario_oficina_id: int,
):
    """Detalle de una usuario-oficina a partir de su id"""
    if current_user.permissions.get("USUARIOS OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        usuario_oficina_id = get_usuario_oficina(db, usuario_oficina_id)
    except MyAnyError as error:
        return OneUsuarioOficinaOut(success=False, message=str(error))
    return OneUsuarioOficinaOut.from_orm(usuario_oficina_id)

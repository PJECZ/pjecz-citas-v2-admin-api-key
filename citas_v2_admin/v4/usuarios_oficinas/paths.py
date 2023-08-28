"""
Usuarios-Oficinas v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_usuario_oficina, get_usuarios_oficinas
from .schemas import OneUsuarioOficinaOut, UsuarioOficinaOut

usuarios_oficinas = APIRouter(prefix="/v4/usuarios_oficinas", tags=["categoria"])


@usuarios_oficinas.get("", response_model=CustomPage[UsuarioOficinaOut])
async def paginado_usuarios_oficinas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    oficina_id: int = None,
    oficina_clave: str = None,
    usuario_id: int = None,
    usuario_email: str = None,
):
    """Paginado de usuarios-oficinas"""
    if current_user.permissions.get("USUARIOS OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_usuarios_oficinas(
            database=database,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
            usuario_id=usuario_id,
            usuario_email=usuario_email,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@usuarios_oficinas.get("/{usuario_oficina_id}", response_model=OneUsuarioOficinaOut)
async def detalle_usuario_oficina(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    usuario_oficina_id: int,
):
    """Detalle de un usuario-oficina a partir de su id"""
    if current_user.permissions.get("USUARIOS OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        usuario_oficina = get_usuario_oficina(database, usuario_oficina_id)
    except MyAnyError as error:
        return OneUsuarioOficinaOut(success=False, message=str(error))
    return OneUsuarioOficinaOut.model_validate(usuario_oficina)

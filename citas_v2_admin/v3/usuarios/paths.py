"""
Usuarios v3, rutas (paths)
"""
from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import DatabaseSession
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import CurrentUser

from .crud import get_usuarios, get_usuario_with_email
from .schemas import UsuarioOut, OneUsuarioOut

usuarios = APIRouter(prefix="/v3/usuarios", tags=["usuarios"])


@usuarios.get("", response_model=CustomPage[UsuarioOut])
async def listado_usuarios(
    current_user: CurrentUser,
    db: DatabaseSession,
    apellido_paterno: str = None,
    apellido_materno: str = None,
    autoridad_id: int = None,
    autoridad_clave: str = None,
    email: str = None,
    nombres: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
):
    """Listado de usuarios"""
    if current_user.permissions.get("USUARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_usuarios(
            db=db,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            autoridad_id=autoridad_id,
            autoridad_clave=autoridad_clave,
            email=email,
            nombres=nombres,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
        )
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@usuarios.get("/{email}", response_model=OneUsuarioOut)
async def detalle_usuario(
    current_user: CurrentUser,
    db: DatabaseSession,
    email: str,
):
    """Detalle de una usuarios a partir de su id"""
    if current_user.permissions.get("USUARIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        usuario = get_usuario_with_email(db, email)
    except MyAnyError as error:
        return OneUsuarioOut(success=False, message=str(error))
    return OneUsuarioOut.from_orm(usuario)

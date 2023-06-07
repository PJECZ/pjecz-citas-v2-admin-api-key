"""
Permisos v3, rutas (paths)
"""
from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import DatabaseSession
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import CurrentUser

from .crud import get_permisos, get_permiso
from .schemas import PermisoOut, OnePermisoOut

permisos = APIRouter(prefix="/v3/permisos", tags=["usuarios"])


@permisos.get("", response_model=CustomPage[PermisoOut])
async def listado_permisos(
    current_user: CurrentUser,
    db: DatabaseSession,
    modulo_id: int = None,
    modulo_nombre: str = None,
    rol_id: int = None,
    rol_nombre: str = None,
):
    """Listado de permisos"""
    if current_user.permissions.get("PERMISOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_permisos(
            db=db,
            modulo_id=modulo_id,
            modulo_nombre=modulo_nombre,
            rol_id=rol_id,
            rol_nombre=rol_nombre,
        )
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@permisos.get("/{permiso_id}", response_model=OnePermisoOut)
async def detalle_permiso(
    current_user: CurrentUser,
    db: DatabaseSession,
    permiso_id: int,
):
    """Detalle de una permisos a partir de su id"""
    if current_user.permissions.get("PERMISOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        permiso = get_permiso(db, permiso_id)
    except MyAnyError as error:
        return OnePermisoOut(success=False, message=str(error))
    return OnePermisoOut.from_orm(permiso)

"""
Modulos v3, rutas (paths)
"""
from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import DatabaseSession
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import CurrentUser

from .crud import get_modulos, get_modulo
from .schemas import ModuloOut, OneModuloOut

modulos = APIRouter(prefix="/v3/modulos", tags=["usuarios"])


@modulos.get("", response_model=CustomPage[ModuloOut])
async def listado_modulos(
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """Listado de modulos"""
    if current_user.permissions.get("MODULOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_modulos(db)
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@modulos.get("/{modulo_id}", response_model=OneModuloOut)
async def detalle_modulo(
    current_user: CurrentUser,
    db: DatabaseSession,
    modulo_id: int,
):
    """Detalle de un modulo a partir de su id"""
    if current_user.permissions.get("MODULOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        modulo = get_modulo(db, modulo_id)
    except MyAnyError as error:
        return OneModuloOut(success=False, message=str(error))
    return OneModuloOut.from_orm(modulo)

"""
Bitacoras v3, rutas (paths)
"""
from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import DatabaseSession
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import CurrentUser

from .crud import get_bitacoras, get_bitacora
from .schemas import BitacoraOut, OneBitacoraOut

bitacoras = APIRouter(prefix="/v3/bitacoras", tags=["usuarios"])


@bitacoras.get("", response_model=CustomPage[BitacoraOut])
async def listado_bitacoras(
    current_user: CurrentUser,
    db: DatabaseSession,
    usuario_id: int = None,
    usuario_email: str = None,
):
    """Listado de bitacoras"""
    if current_user.permissions.get("BITACORAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_bitacoras(db, usuario_id=usuario_id, usuario_email=usuario_email)
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@bitacoras.get("/{bitacora_id}", response_model=OneBitacoraOut)
async def detalle_bitacora(
    current_user: CurrentUser,
    db: DatabaseSession,
    bitacora_id: int,
):
    """Detalle de una bitacoras a partir de su id"""
    if current_user.permissions.get("BITACORAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        bitacora = get_bitacora(db, bitacora_id=bitacora_id)
    except MyAnyError as error:
        return OneBitacoraOut(success=False, message=str(error))
    return OneBitacoraOut.from_orm(bitacora)

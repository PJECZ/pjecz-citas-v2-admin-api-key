"""
Cit Servicios v3, rutas (paths)
"""
from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import DatabaseSession
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import CurrentUser

from .crud import get_cit_servicios, get_cit_servicio
from .schemas import CitServicioOut, OneCitServicioOut

cit_servicios = APIRouter(prefix="/v3/cit_servicios", tags=["citas"])


@cit_servicios.get("", response_model=CustomPage[CitServicioOut])
async def listado_cit_servicios(
    current_user: CurrentUser,
    db: DatabaseSession,
    cit_categoria_id: int = None,
):
    """Listado de servicios"""
    if current_user.permissions.get("CIT SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_servicios(db, cit_categoria_id)
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@cit_servicios.get("/{cit_servicio_id}", response_model=OneCitServicioOut)
async def detalle_cit_servicio_id(
    current_user: CurrentUser,
    db: DatabaseSession,
    cit_servicio_id: int,
):
    """Detalle de una servicio a partir de su id"""
    if current_user.permissions.get("CIT SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_servicio_id = get_cit_servicio(db, cit_servicio_id)
    except MyAnyError as error:
        return OneCitServicioOut(success=False, message=str(error))
    return OneCitServicioOut.from_orm(cit_servicio_id)

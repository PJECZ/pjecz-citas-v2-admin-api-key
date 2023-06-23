"""
Cit Oficinas-Servicios v3, rutas (paths)
"""
from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import DatabaseSession
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import CurrentUser

from .crud import get_cit_oficinas_servicios, get_cit_oficina_servicio
from .schemas import CitOficinaServicioOut, OneCitOficinaServicioOut

cit_oficinas_servicios = APIRouter(prefix="/v3/cit_oficinas_servicios", tags=["categoria"])


@cit_oficinas_servicios.get("", response_model=CustomPage[CitOficinaServicioOut])
async def listado_cit_oficinas_servicios(
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """Listado de oficinas-servicios"""
    if current_user.permissions.get("OFICINAS SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_oficinas_servicios(db)
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@cit_oficinas_servicios.get("/{cit_oficina_servicio_id}", response_model=OneCitOficinaServicioOut)
async def detalle_cit_oficina_servicio_id(
    current_user: CurrentUser,
    db: DatabaseSession,
    cit_oficina_servicio_id: int,
):
    """Detalle de una oficina-servicio a partir de su id"""
    if current_user.permissions.get("OFICINAS SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_oficina_servicio_id = get_cit_oficina_servicio(db, cit_oficina_servicio_id)
    except MyAnyError as error:
        return OneCitOficinaServicioOut(success=False, message=str(error))
    return OneCitOficinaServicioOut.from_orm(cit_oficina_servicio_id)

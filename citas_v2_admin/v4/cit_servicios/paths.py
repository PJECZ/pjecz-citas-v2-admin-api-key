"""
Cit Servicios v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_cit_servicio, get_cit_servicios
from .schemas import CitServicioOut, OneCitServicioOut

cit_servicios = APIRouter(prefix="/v4/cit_servicios", tags=["citas"])


@cit_servicios.get("", response_model=CustomPage[CitServicioOut])
async def paginado_cit_servicios(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_categoria_id: int = None,
):
    """Paginado de servicios"""
    if current_user.permissions.get("CIT SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_servicios(
            database=database,
            cit_categoria_id=cit_categoria_id,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@cit_servicios.get("/{cit_servicio_id}", response_model=OneCitServicioOut)
async def detalle_cit_servicio(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_servicio_id: int,
):
    """Detalle de una servicio a partir de su id"""
    if current_user.permissions.get("CIT SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_servicio = get_cit_servicio(database, cit_servicio_id)
    except MyAnyError as error:
        return OneCitServicioOut(success=False, message=str(error))
    return OneCitServicioOut.model_validate(cit_servicio)

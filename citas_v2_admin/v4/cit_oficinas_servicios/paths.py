"""
Cit Oficinas Servicios v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_cit_oficina_servicio, get_cit_oficinas_servicios
from .schemas import CitOficinaServicioOut, OneCitOficinaServicioOut

cit_oficinas_servicios = APIRouter(prefix="/v4/cit_oficinas_servicios", tags=["citas"])


@cit_oficinas_servicios.get("", response_model=CustomPage[CitOficinaServicioOut])
async def paginado_cit_oficinas_servicios(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_servicio_id: int = None,
    cit_servicio_clave: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
):
    """Paginado de oficinas-servicios"""
    if current_user.permissions.get("CIT OFICINAS SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_oficinas_servicios(
            database=database,
            cit_servicio_id=cit_servicio_id,
            cit_servicio_clave=cit_servicio_clave,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@cit_oficinas_servicios.get("/{cit_oficina_servicio_id}", response_model=OneCitOficinaServicioOut)
async def detalle_cit_oficina_servicio(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_oficina_servicio_id: int,
):
    """Detalle de una oficina-servicio a partir de su id"""
    if current_user.permissions.get("CIT OFICINAS SERVICIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_oficina_servicio = get_cit_oficina_servicio(database, cit_oficina_servicio_id)
    except MyAnyError as error:
        return OneCitOficinaServicioOut(success=False, message=str(error))
    return OneCitOficinaServicioOut.model_validate(cit_oficina_servicio)

"""
Domicilios v3, rutas (paths)
"""
from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import DatabaseSession
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import CurrentUser

from .crud import get_domicilios, get_domicilio
from .schemas import DomicilioOut, OneDomicilioOut

domicilios = APIRouter(prefix="/v3/domicilios", tags=["oficinas"])


@domicilios.get("", response_model=CustomPage[DomicilioOut])
async def listado_domicilios(
    current_user: CurrentUser,
    db: DatabaseSession,
    distrito_id: int = None,
    distrito_clave: str = None,
):
    """Listado de domicilios"""
    if current_user.permissions.get("DOMICILIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_domicilios(
            db=db,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
        )
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@domicilios.get("/{domicilio_id}", response_model=OneDomicilioOut)
async def detalle_domicilio(
    current_user: CurrentUser,
    db: DatabaseSession,
    domicilio_id: int,
):
    """Detalle de una domicilio a partir de su id"""
    if current_user.permissions.get("DOMICILIOS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        domicilio = get_domicilio(db, domicilio_id)
    except MyAnyError as error:
        return OneDomicilioOut(success=False, message=str(error))
    return OneDomicilioOut.from_orm(domicilio)

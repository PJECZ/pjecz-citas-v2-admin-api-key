"""
Cit Clientes Recuperaciones v3, rutas (paths)
"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from config.settings import Settings, get_settings
from lib.database import DatabaseSession
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import CurrentUser

from .crud import get_cit_clientes_recuperaciones, get_cit_cliente_recuperacion
from .schemas import CitClienteRecuperacionOut, OneCitClienteRecuperacionOut

cit_clientes_recuperaciones = APIRouter(prefix="/v3/cit_clientes_recuperaciones", tags=["categoria"])


@cit_clientes_recuperaciones.get("", response_model=CustomPage[CitClienteRecuperacionOut])
async def listado_cit_clientes_recuperaciones(
    current_user: CurrentUser,
    db: DatabaseSession,
    settings: Settings = Depends(get_settings),
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    ya_recuperado: bool = None,
):
    """Listado de recuperaciones"""
    if current_user.permissions.get("CIT CLIENTES RECUPERACIONES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_clientes_recuperaciones(
            db=db,
            cit_cliente_id=cit_cliente_id,
            cit_cliente_email=cit_cliente_email,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            settings=settings,
            ya_recuperado=ya_recuperado,
        )
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@cit_clientes_recuperaciones.get("/{cit_cliente_recuperacion_id}", response_model=OneCitClienteRecuperacionOut)
async def detalle_cit_cliente_recuperacion_id(
    current_user: CurrentUser,
    db: DatabaseSession,
    cit_cliente_recuperacion_id: int,
):
    """Detalle de una recuperacion a partir de su id"""
    if current_user.permissions.get("CIT CLIENTES RECUPERACIONES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cliente_recuperacion_id = get_cit_cliente_recuperacion(db, cit_cliente_recuperacion_id)
    except MyAnyError as error:
        return OneCitClienteRecuperacionOut(success=False, message=str(error))
    return OneCitClienteRecuperacionOut.from_orm(cit_cliente_recuperacion_id)

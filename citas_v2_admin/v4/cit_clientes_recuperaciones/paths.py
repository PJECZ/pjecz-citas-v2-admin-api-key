"""
Cit Clientes Recuperaciones v4, rutas (paths)
"""
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_cit_cliente_recuperacion, get_cit_clientes_recuperaciones
from .schemas import CitClienteRecuperacionOut, OneCitClienteRecuperacionOut

cit_clientes_recuperaciones = APIRouter(prefix="/v4/cit_clientes_recuperaciones", tags=["citas"])


@cit_clientes_recuperaciones.get("", response_model=CustomPage[CitClienteRecuperacionOut])
async def paginado_cit_clientes_recuperaciones(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_cliente_id: int = None,
    cit_cliente_curp: str = None,
    cit_cliente_email: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    ya_recuperado: bool = None,
):
    """Paginado de clientes recuperaciones"""
    if current_user.permissions.get("CIT CLIENTES RECUPERACIONES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_clientes_recuperaciones(
            database=database,
            cit_cliente_id=cit_cliente_id,
            cit_cliente_curp=cit_cliente_curp,
            cit_cliente_email=cit_cliente_email,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            ya_recuperado=ya_recuperado,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@cit_clientes_recuperaciones.get("/{cit_cliente_recuperacion_id}", response_model=OneCitClienteRecuperacionOut)
async def detalle_cit_cliente_recuperacion(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_cliente_recuperacion_id: int,
):
    """Detalle de una cliente recuperacion a partir de su id"""
    if current_user.permissions.get("CIT CLIENTES RECUPERACIONES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cliente_recuperacion = get_cit_cliente_recuperacion(database, cit_cliente_recuperacion_id)
    except MyAnyError as error:
        return OneCitClienteRecuperacionOut(success=False, message=str(error))
    return OneCitClienteRecuperacionOut.model_validate(cit_cliente_recuperacion)

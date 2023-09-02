"""
Cit Clientes Registros v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_cit_cliente_registro, get_cit_clientes_registros
from .schemas import CitClienteRegistroOut, OneCitClienteRegistroOut

cit_clientes_registros = APIRouter(prefix="/v4/cit_clientes_registros", tags=["citas"])


@cit_clientes_registros.get("", response_model=CustomPage[CitClienteRegistroOut])
async def paginado_cit_clientes_registros(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de clientes registros"""
    if current_user.permissions.get("CIT CLIENTES REGISTROS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_clientes_registros(database)
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@cit_clientes_registros.get("/{cit_cliente_registro_id}", response_model=OneCitClienteRegistroOut)
async def detalle_cit_cliente_registro(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_cliente_registro_id: int,
):
    """Detalle de una cliente registro a partir de su id"""
    if current_user.permissions.get("CIT CLIENTES REGISTROS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cliente_registro = get_cit_cliente_registro(database, cit_cliente_registro_id)
    except MyAnyError as error:
        return OneCitClienteRegistroOut(success=False, message=str(error))
    return OneCitClienteRegistroOut.model_validate(cit_cliente_registro)

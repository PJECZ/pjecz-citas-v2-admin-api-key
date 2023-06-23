"""
Cit Clientes Registros v3, rutas (paths)
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

from .crud import get_cit_clientes_registros, get_cit_cliente_registro
from .schemas import CitClienteRegistroOut, OneCitClienteRegistroOut

cit_clientes_registros = APIRouter(prefix="/v3/cit_clientes_registros", tags=["citas"])


@cit_clientes_registros.get("", response_model=CustomPage[CitClienteRegistroOut])
async def listado_cit_clientes_registros(
    current_user: CurrentUser,
    db: DatabaseSession,
    settings: Settings = Depends(get_settings),
    apellido_primero: str = None,
    apellido_segundo: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    curp: str = None,
    email: str = None,
    nombres: str = None,
    ya_registrado: bool = None,
):
    """Listado de registros de clientes"""
    if current_user.permissions.get("CIT CLIENTES REGISTROS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_clientes_registros(
            db=db,
            apellido_primero=apellido_primero,
            apellido_segundo=apellido_segundo,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            curp=curp,
            email=email,
            nombres=nombres,
            ya_registrado=ya_registrado,
            settings=settings,
        )
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@cit_clientes_registros.get("/{cit_cliente_registro_id}", response_model=OneCitClienteRegistroOut)
async def detalle_cit_cliente_registro_id(
    current_user: CurrentUser,
    db: DatabaseSession,
    cit_cliente_registro_id: int,
):
    """Detalle de una registro de cliente a partir de su id"""
    if current_user.permissions.get("CIT CLIENTES REGISTROS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cliente_registro_id = get_cit_cliente_registro(db, cit_cliente_registro_id)
    except MyAnyError as error:
        return OneCitClienteRegistroOut(success=False, message=str(error))
    return OneCitClienteRegistroOut.from_orm(cit_cliente_registro_id)

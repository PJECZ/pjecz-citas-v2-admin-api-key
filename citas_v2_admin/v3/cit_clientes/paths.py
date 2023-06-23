"""
Cit Clientes v3, rutas (paths)
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

from .crud import get_cit_clientes, get_cit_cliente
from .schemas import CitClienteOut, OneCitClienteOut

cit_clientes = APIRouter(prefix="/v3/cit_clientes", tags=["categoria"])


@cit_clientes.get("", response_model=CustomPage[CitClienteOut])
async def listado_cit_clientes(
    current_user: CurrentUser,
    db: DatabaseSession,
    settings: Settings = Depends(get_settings),
    apellido_primero: str = None,
    apellido_segundo: str = None,
    autoriza_mensajes: bool = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    curp: str = None,
    email: str = None,
    enviar_boletin: bool = None,
    nombres: str = None,
    telefono: str = None,
    tiene_contrasena_sha256: bool = None,
):
    """Listado de clientes"""
    if current_user.permissions.get("CIT CLIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_clientes(
            db=db,
            apellido_primero=apellido_primero,
            apellido_segundo=apellido_segundo,
            autoriza_mensajes=autoriza_mensajes,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            curp=curp,
            email=email,
            enviar_boletin=enviar_boletin,
            nombres=nombres,
            settings=settings,
            telefono=telefono,
            tiene_contrasena_sha256=tiene_contrasena_sha256,
        )
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@cit_clientes.get("/{cit_cliente_id}", response_model=OneCitClienteOut)
async def detalle_cit_cliente_id(
    current_user: CurrentUser,
    db: DatabaseSession,
    cit_cliente_id: int,
):
    """Detalle de un cliente a partir de su id"""
    if current_user.permissions.get("CIT CLIENTES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cliente_id = get_cit_cliente(db, cit_cliente_id)
    except MyAnyError as error:
        return OneCitClienteOut(success=False, message=str(error))
    return OneCitClienteOut.from_orm(cit_cliente_id)

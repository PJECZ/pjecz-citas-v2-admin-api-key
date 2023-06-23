"""
Cit Citas v3, rutas (paths)
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

from .crud import get_cit_citas, get_cit_cita
from .schemas import CitCitaOut, OneCitCitaOut

cit_citas = APIRouter(prefix="/v3/cit_citas", tags=["citas"])


@cit_citas.get("", response_model=CustomPage[CitCitaOut])
async def listado_cit_citas(
    current_user: CurrentUser,
    db: DatabaseSession,
    settings: Settings = Depends(get_settings),
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    cit_servicio_id: int = None,
    cit_servicio_clave: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    inicio: date = None,
    inicio_desde: date = None,
    inicio_hasta: date = None,
    estado: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
):
    """Listado de citas"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_citas(
            db=db,
            cit_cliente_id=cit_cliente_id,
            cit_cliente_email=cit_cliente_email,
            cit_servicio_id=cit_servicio_id,
            cit_servicio_clave=cit_servicio_clave,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            inicio=inicio,
            inicio_desde=inicio_desde,
            inicio_hasta=inicio_hasta,
            estado=estado,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
            settings=settings,
        )
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@cit_citas.get("/{cit_cita_id}", response_model=OneCitCitaOut)
async def detalle_cit_cita_id(
    current_user: CurrentUser,
    db: DatabaseSession,
    cit_cita_id: int,
):
    """Detalle de una cita a partir de su id"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cita_id = get_cit_cita(db, cit_cita_id)
    except MyAnyError as error:
        return OneCitCitaOut(success=False, message=str(error))
    return OneCitCitaOut.from_orm(cit_cita_id)

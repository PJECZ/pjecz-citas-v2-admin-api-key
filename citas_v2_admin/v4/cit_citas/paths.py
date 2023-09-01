"""
Cit Citas v4, rutas (paths)
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
from .crud import get_cit_cita, get_cit_citas
from .schemas import CitCitaOut, OneCitCitaOut

cit_citas = APIRouter(prefix="/v4/cit_citas", tags=["categoria"])


@cit_citas.get("", response_model=CustomPage[CitCitaOut])
async def paginado_cit_citas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_cliente_id: int = None,
    cit_cliente_curp: str = None,
    cit_cliente_email: str = None,
    cit_servicio_id: int = None,
    cit_servicio_clave: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    estado: str = None,
    inicio: date = None,
    inicio_desde: date = None,
    inicio_hasta: date = None,
    oficina_id: int = None,
    oficina_clave: str = None,
):
    """Paginado de citas"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_citas(
            database=database,
            cit_cliente_id=cit_cliente_id,
            cit_cliente_curp=cit_cliente_curp,
            cit_cliente_email=cit_cliente_email,
            cit_servicio_id=cit_servicio_id,
            cit_servicio_clave=cit_servicio_clave,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            estado=estado,
            inicio=inicio,
            inicio_desde=inicio_desde,
            inicio_hasta=inicio_hasta,
            oficina_id=oficina_id,
            oficina_clave=oficina_clave,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@cit_citas.get("/{cit_cita_id}", response_model=OneCitCitaOut)
async def detalle_cit_cita(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_cita_id: int,
):
    """Detalle de una cita a partir de su id"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cita = get_cit_cita(database, cit_cita_id)
    except MyAnyError as error:
        return OneCitCitaOut(success=False, message=str(error))
    return OneCitCitaOut.model_validate(cit_cita)

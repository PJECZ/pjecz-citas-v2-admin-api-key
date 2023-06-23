"""
Cit Horas Bloqueadas v3, rutas (paths)
"""
from datetime import date

from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import DatabaseSession
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import CurrentUser

from .crud import get_cit_horas_bloqueadas, get_cit_hora_bloqueada
from .schemas import CitHoraBloqueadaOut, OneCitHoraBloqueadaOut

cit_horas_bloqueadas = APIRouter(prefix="/v3/cit_horas_bloqueadas", tags=["categoria"])


@cit_horas_bloqueadas.get("", response_model=CustomPage[CitHoraBloqueadaOut])
async def listado_cit_horas_bloqueadas(
    current_user: CurrentUser,
    db: DatabaseSession,
    fecha: date = None,
    oficina_id: int = None,
):
    """Listado de horas bloqueadas"""
    if current_user.permissions.get("CIT HORAS BLOQUEADAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_horas_bloqueadas(
            db=db,
            fecha=fecha,
            oficina_id=oficina_id,
        )
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@cit_horas_bloqueadas.get("/{cit_hora_bloqueada_id}", response_model=OneCitHoraBloqueadaOut)
async def detalle_cit_hora_bloqueada_id(
    current_user: CurrentUser,
    db: DatabaseSession,
    cit_hora_bloqueada_id: int,
):
    """Detalle de una hora bloqueada a partir de su id"""
    if current_user.permissions.get("CIT HORAS BLOQUEADAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_hora_bloqueada_id = get_cit_hora_bloqueada(db, cit_hora_bloqueada_id)
    except MyAnyError as error:
        return OneCitHoraBloqueadaOut(success=False, message=str(error))
    return OneCitHoraBloqueadaOut.from_orm(cit_hora_bloqueada_id)

"""
Cit Horas Bloqueadas v4, rutas (paths)
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
from .crud import get_cit_hora_bloqueada, get_cit_horas_bloqueadas
from .schemas import CitHoraBloqueadaOut, OneCitHoraBloqueadaOut

cit_horas_bloqueadas = APIRouter(prefix="/v4/cit_horas_bloqueadas", tags=["citas"])


@cit_horas_bloqueadas.get("", response_model=CustomPage[CitHoraBloqueadaOut])
async def paginado_cit_horas_bloqueadas(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    fecha: date,
    oficina_id: int,
):
    """Paginado de horas bloqueadas"""
    if current_user.permissions.get("CIT HORAS BLOQUEADAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_horas_bloqueadas(
            database=database,
            fecha=fecha,
            oficina_id=oficina_id,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@cit_horas_bloqueadas.get("/{cit_hora_bloqueada_id}", response_model=OneCitHoraBloqueadaOut)
async def detalle_cit_hora_bloqueada(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_hora_bloqueada_id: int,
):
    """Detalle de una hora bloqueada a partir de su id"""
    if current_user.permissions.get("CIT HORAS BLOQUEADAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_hora_bloqueada = get_cit_hora_bloqueada(database, cit_hora_bloqueada_id)
    except MyAnyError as error:
        return OneCitHoraBloqueadaOut(success=False, message=str(error))
    return OneCitHoraBloqueadaOut.model_validate(cit_hora_bloqueada)

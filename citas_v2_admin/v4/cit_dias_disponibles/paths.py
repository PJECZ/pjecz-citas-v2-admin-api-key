"""
Cit Dias Disponibles v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_cit_dia_disponible, get_cit_dias_disponibles
from .schemas import CitDiaDisponibleOut, OneCitDiaDisponibleOut

cit_dias_disponibles = APIRouter(prefix="/v4/cit_dias_disponibles", tags=["categoria"])


@cit_dias_disponibles.get("", response_model=CustomPage[CitDiaDisponibleOut])
async def paginado_cit_dias_disponibles(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    size: int = 100,
):
    """Paginado de dias disponibles"""
    if current_user.permissions.get("CIT DIAS DISPONIBLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_dias_disponibles(
            database=database,
            size=size,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@cit_dias_disponibles.get("/proximo", response_model=OneCitDiaDisponibleOut)
async def detalle_cit_dia_disponible(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """El proximo dia disponible"""
    if current_user.permissions.get("CIT DIAS DISPONIBLES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_dia_disponible = get_cit_dia_disponible(database)
    except MyAnyError as error:
        return OneCitDiaDisponibleOut(success=False, message=str(error))
    return OneCitDiaDisponibleOut.model_validate(cit_dia_disponible)

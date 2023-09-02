"""
Cit Dias Disponibles v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_list import CustomList

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_cit_dia_disponible, get_cit_dias_disponibles
from .schemas import CitDiaDisponibleOut, OneCitDiaDisponibleOut

cit_dias_disponibles = APIRouter(prefix="/v4/cit_dias_disponibles", tags=["citas"])


@cit_dias_disponibles.get("", response_model=CustomList[CitDiaDisponibleOut])
async def paginado_cit_dias_disponibles(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    size: int = 100,
):
    """Listado de dias disponibles"""
    if current_user.permissions.get("CIT DIAS INHABILES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_dias_disponibles(
            database=database,
            size=size,
        )
    except MyAnyError as error:
        return CustomList(success=False, message=str(error))
    lista = [CitDiaDisponibleOut(fecha=item) for item in resultados]
    return CustomList(items=lista, message="Success", success=True, total=len(lista), page=1, size=size, pages=1)


@cit_dias_disponibles.get("/proximo", response_model=OneCitDiaDisponibleOut)
async def detalle_cit_dia_disponible(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """El proximo dia disponible"""
    if current_user.permissions.get("CIT DIAS INHABILES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_dia_disponible = get_cit_dia_disponible(database)
    except MyAnyError as error:
        return OneCitDiaDisponibleOut(success=False, message=str(error))
    return OneCitDiaDisponibleOut(fecha=cit_dia_disponible, message="Success", success=True)

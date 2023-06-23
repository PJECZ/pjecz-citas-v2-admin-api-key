"""
Cit Dias Disponibles v3, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status

from config.settings import Settings, get_settings
from lib.database import DatabaseSession
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_list import CustomList, ListResult, custom_list_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import CurrentUser

from .crud import get_cit_dias_disponibles, get_cit_dia_disponible
from .schemas import CitDiaDisponibleOut, OneCitDiaDisponibleOut

cit_dias_disponibles = APIRouter(prefix="/v3/cit_dias_disponibles", tags=["categoria"])


@cit_dias_disponibles.get("", response_model=CustomList[CitDiaDisponibleOut])
async def listado_cit_dias_disponibles(
    current_user: CurrentUser,
    db: DatabaseSession,
    settings: Settings = Depends(get_settings),
    size: int = 100,
):
    """Listado de dias disponibles"""
    if current_user.permissions.get("CIT DIAS INHABILES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_dias_disponibles(
            db=db,
            settings=settings,
            size=size,
        )
    except MyAnyError as error:
        return custom_list_success_false(error)
    items = [CitDiaDisponibleOut(fecha=item) for item in resultados]
    result = ListResult(total=len(items), items=items, size=size)
    return CustomList(result=result)


@cit_dias_disponibles.get("/proximo", response_model=OneCitDiaDisponibleOut)
async def detalle_cit_dia_disponible_id(
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """Proximo dia disponible sin tomar en cuenta la hora"""
    if current_user.permissions.get("CIT DIAS INHABILES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    fecha = get_cit_dia_disponible(db=db)
    return OneCitDiaDisponibleOut(fecha=fecha)

"""
Cit Horas Disponibles v3, rutas (paths)
"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status

from config.settings import Settings, get_settings
from lib.database import DatabaseSession
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_list import CustomList, ListResult, custom_list_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import CurrentUser

from .crud import get_cit_horas_disponibles
from .schemas import CitHoraDisponibleOut

cit_horas_disponibles = APIRouter(prefix="/v3/cit_horas_disponibles", tags=["categoria"])


@cit_horas_disponibles.get("", response_model=CustomList[CitHoraDisponibleOut])
async def listado_cit_horas_disponibles(
    current_user: CurrentUser,
    db: DatabaseSession,
    cit_servicio_id: int,
    fecha: date,
    oficina_id: int,
    settings: Settings = Depends(get_settings),
    size: int = 100,
):
    """Listado de horas disponibles"""
    if current_user.permissions.get("CIT HORAS BLOQUEADAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_horas_disponibles(
            db=db,
            cit_servicio_id=cit_servicio_id,
            fecha=fecha,
            oficina_id=oficina_id,
            settings=settings,
            size=size,
        )
    except MyAnyError as error:
        return custom_list_success_false(error)
    items = [CitHoraDisponibleOut(horas_minutos=item) for item in resultados]
    result = ListResult(total=len(items), items=items, size=size)
    return CustomList(result=result)

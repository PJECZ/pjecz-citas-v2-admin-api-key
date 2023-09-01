"""
Cit Horas Disponibles v4, rutas (paths)
"""
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_list import CustomList

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_cit_horas_disponibles
from .schemas import CitHoraDisponibleOut

cit_horas_disponibles = APIRouter(prefix="/v4/cit_horas_disponibles", tags=["categoria"])


@cit_horas_disponibles.get("", response_model=CustomList[CitHoraDisponibleOut])
async def paginado_cit_horas_disponibles(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_servicio_id: int,
    fecha: date,
    oficina_id: int,
    size: int = 100,
):
    """Listado de horas disponibles"""
    if current_user.permissions.get("CIT HORAS BLOQUEADAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_horas_disponibles(
            database=database,
            cit_servicio_id=cit_servicio_id,
            fecha=fecha,
            oficina_id=oficina_id,
            size=size,
        )
    except MyAnyError as error:
        return CustomList(success=False, message=str(error))
    lista = [CitHoraDisponibleOut(horas_minutos=item) for item in resultados]
    return CustomList(items=lista, message="Success", success=True, total=len(lista), page=1, size=size, pages=1)

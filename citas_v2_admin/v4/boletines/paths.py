"""
Boletines v4, rutas (paths)
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
from .crud import get_boletin, get_boletines
from .schemas import BoletinOut, OneBoletinOut

boletines = APIRouter(prefix="/v4/boletines", tags=["categoria"])


@boletines.get("", response_model=CustomPage[BoletinOut])
async def paginado_boletines(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    estado: str = None,
    envio_programado_desde: date = None,
    envio_programado_hasta: date = None,
):
    """Paginado de boletines"""
    if current_user.permissions.get("BOLETINES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_boletines(
            database=database,
            estado=estado,
            envio_programado_desde=envio_programado_desde,
            envio_programado_hasta=envio_programado_hasta,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@boletines.get("/{boletin_id}", response_model=OneBoletinOut)
async def detalle_boletin(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    boletin: int,
):
    """Detalle de un boletin a partir de su id"""
    if current_user.permissions.get("BOLETINES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        boletin = get_boletin(database, boletin)
    except MyAnyError as error:
        return OneBoletinOut(success=False, message=str(error))
    return OneBoletinOut.model_validate(boletin)

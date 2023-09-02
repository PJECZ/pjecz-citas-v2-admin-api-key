"""
Cit Dias Inhabiles v4, rutas (paths)
"""
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.cit_dias_inhabiles.models import CitDiaInhabil
from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import create_cit_dia_inhabil, delete_cit_dia_inhabil, get_cit_dia_inhabil_with_fecha, get_cit_dias_inhabiles, update_cit_dia_inhabil
from .schemas import CitDiaInhabilIn, CitDiaInhabilOut, OneCitDiaInhabilOut

cit_dias_inhabiles = APIRouter(prefix="/v4/cit_dias_inhabiles", tags=["categoria"])


@cit_dias_inhabiles.get("", response_model=CustomPage[CitDiaInhabilOut])
async def paginado_cit_dias_inhabiles(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    fecha_desde: date = None,
    fecha_hasta: date = None,
):
    """Paginado de dias inhabiles"""
    if current_user.permissions.get("CIT DIAS INHABILES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_dias_inhabiles(
            database=database,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@cit_dias_inhabiles.get("/{fecha}", response_model=OneCitDiaInhabilOut)
async def detalle_cit_dia_inhabil(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    fecha: date,
):
    """Detalle de una dia inhabil a partir de su id"""
    if current_user.permissions.get("CIT DIAS INHABILES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_dia_inhabil = get_cit_dia_inhabil_with_fecha(database, fecha)
    except MyAnyError as error:
        return OneCitDiaInhabilOut(success=False, message=str(error))
    return OneCitDiaInhabilOut.model_validate(cit_dia_inhabil)


@cit_dias_inhabiles.post("", response_model=CitDiaInhabilOut)
async def crear_cit_dia_inhabil(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_dia_inhabil_in: CitDiaInhabilIn,
):
    """Crear un dia inhabil"""
    if current_user.permissions.get("CIT DIAS INHABILES", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_dia_inhabil = create_cit_dia_inhabil(database, CitDiaInhabil(**cit_dia_inhabil_in.model_dump()))
    except MyAnyError as error:
        return CitDiaInhabilOut(success=False, message=str(error))
    respuesta = CitDiaInhabilOut.model_validate(cit_dia_inhabil)
    respuesta.message = "Dia inhabil creado correctamente"
    return respuesta


@cit_dias_inhabiles.put("/{cit_dia_inhabil_id}", response_model=CitDiaInhabilOut)
async def modificar_cit_dia_inhabil(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_dia_inhabil_id: int,
    cit_dia_inhabil_in: CitDiaInhabilIn,
):
    """Modificar un dia inhabil"""
    if current_user.permissions.get("CIT DIAS INHABILES", 0) < Permiso.MODIFICAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_dia_inhabil = update_cit_dia_inhabil(database, cit_dia_inhabil_id, CitDiaInhabil(**cit_dia_inhabil_in.model_dump()))
    except MyAnyError as error:
        return CitDiaInhabilOut(success=False, message=str(error))
    respuesta = CitDiaInhabilOut.model_validate(cit_dia_inhabil)
    respuesta.message = "Dia inhabil modificado correctamente"
    return respuesta


@cit_dias_inhabiles.delete("/{cit_dia_inhabil_id}", response_model=CitDiaInhabilOut)
async def borrar_cit_dia_inhabil(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_dia_inhabil_id: int,
):
    """Borrar un dia inhabil"""
    if current_user.permissions.get("CIT DIAS INHABILES", 0) < Permiso.BORRAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_dia_inhabil = delete_cit_dia_inhabil(database, cit_dia_inhabil_id)
    except MyAnyError as error:
        return CitDiaInhabilOut(success=False, message=str(error))
    respuesta = CitDiaInhabilOut.model_validate(cit_dia_inhabil)
    respuesta.message = "Dia inhabil borrado correctamente"
    return respuesta

"""
Cit Citas v4, rutas (paths)
"""
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_list import CustomList
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import (
    cancel_cit_cita,
    create_cit_cita,
    get_cit_cita,
    get_cit_citas,
    get_cit_citas_agendadas_por_servicio_oficina,
    get_cit_citas_creados_por_dia,
    get_cit_citas_creados_por_dia_distrito,
)
from .schemas import (
    CitCitaIn,
    CitCitaOut,
    CitCitasAgendadasPorServicioOficinaOut,
    CitCitasCreadosPorDiaDistritoOut,
    CitCitasCreadosPorDiaOut,
    OneCitCitaOut,
)

cit_citas = APIRouter(prefix="/v4/cit_citas", tags=["citas"])


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


@cit_citas.get("/cit_citas_agendadas_por_servicio_oficina", response_model=CustomList[CitCitasAgendadasPorServicioOficinaOut])
async def listado_cit_citas_agendadas_por_servicio_oficina(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    inicio: date = None,
    inicio_desde: date = None,
    inicio_hasta: date = None,
    size: int = 100,
):
    """Listado de servicios y oficinas con cantidades de citas agendadas"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_citas_agendadas_por_servicio_oficina(
            database=database,
            inicio=inicio,
            inicio_desde=inicio_desde,
            inicio_hasta=inicio_hasta,
            size=size,
        )
    except MyAnyError as error:
        return CustomList(success=False, message=str(error))
    lista = []
    for item in resultados:
        CitCitasAgendadasPorServicioOficinaOut(oficina=item.oficina, servicio=item.servicio, cantidad=item.cantidad)
    return CustomList(items=lista, message="Success", success=True, total=len(lista), page=1, size=size, pages=1)


@cit_citas.get("/creados_por_dia", response_model=CustomList[CitCitasCreadosPorDiaOut])
async def listado_cit_citas_creados_por_dia(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    size: int = 100,
):
    """Listado de fechas y cantidades de citas creadas por dia"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_citas_creados_por_dia(
            database=database,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            size=size,
        )
    except MyAnyError as error:
        return CustomList(success=False, message=str(error))
    lista = []
    for item in resultados:
        CitCitasCreadosPorDiaOut(creado=item.creado, cantidad=item.cantidad)
    return CustomList(items=lista, message="Success", success=True, total=len(lista), page=1, size=size, pages=1)


@cit_citas.get("/cit_citas_creados_por_dia_distrito", response_model=CustomList[CitCitasCreadosPorDiaDistritoOut])
async def listado_cit_citas_creados_por_dia_distrito(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    size: int = 100,
):
    """Listado de fechas y cantidades de citas por dia y distrito"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_citas_creados_por_dia_distrito(
            database=database,
            creado=creado,
            creado_desde=creado_desde,
            creado_hasta=creado_hasta,
            size=size,
        )
    except MyAnyError as error:
        return CustomList(success=False, message=str(error))
    lista = []
    for item in resultados:
        CitCitasCreadosPorDiaDistritoOut(creado=item.creado, distrito=item.distrito, cantidad=item.cantidad)
    return CustomList(items=lista, message="Success", success=True, total=len(lista), page=1, size=size, pages=1)


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


@cit_citas.put("/cancelar/{cit_cita_id}", response_model=OneCitCitaOut)
async def cancelar_cit_cita(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_cita_id: int,
):
    """Cancelar una cita"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cita = cancel_cit_cita(database, cit_cita_id)
    except MyAnyError as error:
        return OneCitCitaOut(success=False, message=str(error))
    respuesta = OneCitCitaOut.model_validate(cit_cita)
    respuesta.message = "Cita cancelada correctamente"
    return respuesta


@cit_citas.post("", response_model=OneCitCitaOut)
async def crear_cit_cita(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_cita_in: CitCitaIn,
):
    """Crear una cita"""
    if current_user.permissions.get("CIT CITAS", 0) < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cita = create_cit_cita(
            database=database,
            cit_cliente_id=cit_cita_in.cit_cliente_id,
            cit_servicio_id=cit_cita_in.cit_servicio_id,
            fecha=cit_cita_in.fecha,
            hora_minuto=cit_cita_in.hora_minuto,
            oficina_id=cit_cita_in.oficina_id,
            notas=cit_cita_in.notas,
        )
    except MyAnyError as error:
        return OneCitCitaOut(success=False, message=str(error))
    respuesta = OneCitCitaOut.model_validate(cit_cita)
    respuesta.message = "Cita creada correctamente"
    return respuesta

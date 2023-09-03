"""
Cit Clientes v4, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import count, func

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_curp, safe_email, safe_string, safe_telefono

from ...core.cit_clientes.models import CitCliente


def get_cit_clientes(
    database: Session,
    apellido_primero: str = None,
    apellido_segundo: str = None,
    autoriza_mensajes: bool = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    curp: str = None,
    email: str = None,
    enviar_boletin: bool = None,
    nombres: str = None,
    telefono: str = None,
    tiene_contrasena_sha256: bool = None,
) -> Any:
    """Consultar los clientes activos"""
    consulta = database.query(CitCliente)

    # Filtrar por apellido primero
    if apellido_primero is not None:
        apellido_primero = safe_string(apellido_primero)
        if apellido_primero != "":
            consulta = consulta.filter(CitCliente.apellido_primero.contains(apellido_primero))

    # Filtrar por apellido segundo
    if apellido_segundo is not None:
        apellido_segundo = safe_string(apellido_segundo)
        if apellido_segundo != "":
            consulta = consulta.filter(CitCliente.apellido_segundo.contains(apellido_segundo))

    # Filtrar por autoriza mensajes
    if autoriza_mensajes is not None:
        consulta = consulta.filter(CitCliente.autoriza_mensajes == autoriza_mensajes)

    # Filtrar por creado
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(CitCliente.creado >= desde_dt).filter(CitCliente.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0)
        consulta = consulta.filter(CitCliente.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(CitCliente.creado <= hasta_dt)

    # Filtrar por fragmento de CURP
    if curp is not None:
        try:
            curp = safe_curp(curp, search_fragment=True)
        except ValueError as error:
            raise MyNotValidParamError("No es un CURP válido") from error
        consulta = consulta.filter(CitCliente.curp.contains(curp))

    # Filtrar por fragmento de email
    if email is not None:
        try:
            email = safe_email(email, search_fragment=True)
        except ValueError as error:
            raise MyNotValidParamError("No es un email válido") from error
        consulta = consulta.filter(CitCliente.email.contains(email))

    # Filtrar por enviar boletin
    if enviar_boletin is not None:
        consulta = consulta.filter(CitCliente.enviar_boletin == enviar_boletin)

    # Filtrar por nombres
    if nombres is not None:
        nombres = safe_string(nombres)
        if nombres != "":
            consulta = consulta.filter(CitCliente.nombres.contains(nombres))

    # Filtrar por telefono
    if telefono is not None:
        try:
            telefono = safe_telefono(telefono)
        except ValueError as error:
            raise MyNotValidParamError("No es un telefono válido") from error
        consulta = consulta.filter(CitCliente.telefono.contains(telefono))

    # Filtrar por contrasena sha256
    if tiene_contrasena_sha256 is not None:
        if tiene_contrasena_sha256:
            consulta = consulta.filter(CitCliente.contrasena_sha256 != "")
        else:
            consulta = consulta.filter(CitCliente.contrasena_sha256 == "")

    # Entregar
    return consulta.filter_by(estatus="A").order_by(CitCliente.id)


def get_cit_cliente(database: Session, cit_cliente_id: int) -> CitCliente:
    """Consultar un cliente por su id"""
    cit_cliente = database.query(CitCliente).get(cit_cliente_id)
    if cit_cliente is None:
        raise MyNotExistsError("No existe ese cliente")
    if cit_cliente.estatus != "A":
        raise MyIsDeletedError("No es activo ese cliente, está eliminado")
    return cit_cliente


def get_cit_cliente_with_curp(database: Session, curp: str) -> CitCliente:
    """Consultar un cliente por su curp"""
    try:
        curp = safe_curp(curp, search_fragment=False)
    except ValueError as error:
        raise MyNotValidParamError("No es un CURP válido") from error
    cit_cliente = database.query(CitCliente).filter_by(curp=curp).first()
    if cit_cliente is None:
        raise MyNotExistsError("No existe ese cliente")
    if cit_cliente.estatus != "A":
        raise MyIsDeletedError("No es activo ese cliente, está eliminado")
    return cit_cliente


def get_cit_cliente_with_email(database: Session, email: str) -> CitCliente:
    """Consultar un cliente por su email"""
    try:
        email = safe_email(email, search_fragment=False)
    except ValueError as error:
        raise MyNotValidParamError("No es un email válido") from error
    cit_cliente = database.query(CitCliente).filter_by(email=email).first()
    if cit_cliente is None:
        raise MyNotExistsError("No existe ese cliente")
    if cit_cliente.estatus != "A":
        raise MyIsDeletedError("No es activo ese cliente, está eliminado")
    return cit_cliente


def get_cit_clientes_creados_por_dia(
    database: Session,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    size: int = 100,
) -> Any:
    """Consultar las cantidades de citas creadas por dia"""

    # Observe que para la columna `creado` se usa la función func.date()
    consulta = database.query(
        func.date(CitCliente.creado).label("creado"),
        count(CitCliente.id).label("cantidad"),
    )

    # Si no vienen creado, creado_desde, creado_hasta, se usa el size como cantidad de dias
    if creado is None and creado_desde is None and creado_hasta is None:
        hoy = date.today()
        creado_desde = hoy - timedelta(days=size)
        creado_hasta = hoy
    elif creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(CitCliente.creado >= desde_dt).filter(CitCliente.creado <= hasta_dt)
    else:
        if creado_desde is not None:
            desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0)
            consulta = consulta.filter(CitCliente.creado >= desde_dt)
        if creado_hasta is not None:
            hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59)
            consulta = consulta.filter(CitCliente.creado <= hasta_dt)

    # Agrupar por creado y entregar
    return consulta.group_by(func.date(CitCliente.creado))

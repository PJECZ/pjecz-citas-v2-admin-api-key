"""
Cit Citas v4, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import count, func

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_string

from ...core.cit_citas.models import CitCita
from ...core.cit_servicios.models import CitServicio
from ...core.distritos.models import Distrito
from ...core.oficinas.models import Oficina
from ..cit_clientes.crud import get_cit_cliente, get_cit_cliente_with_curp, get_cit_cliente_with_email
from ..cit_servicios.crud import get_cit_servicio, get_cit_servicio_with_clave
from ..oficinas.crud import get_oficina, get_oficina_with_clave


def get_cit_citas(
    database: Session,
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
) -> Any:
    """Consultar las citas activas"""
    consulta = database.query(CitCita)

    # Filtrar por cliente
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(database, cit_cliente_id)
        consulta = consulta.filter_by(cit_cliente_id=cit_cliente.id)
    elif cit_cliente_curp is not None:
        cit_cliente = get_cit_cliente_with_curp(database, cit_cliente_curp)
        consulta = consulta.filter_by(cit_cliente_id=cit_cliente.id)
    elif cit_cliente_email is not None:
        cit_cliente = get_cit_cliente_with_email(database, cit_cliente_email)
        consulta = consulta.filter_by(cit_cliente_id=cit_cliente.id)

    # Filtrar por servicio
    if cit_servicio_id is not None:
        cit_servicio = get_cit_servicio(database, cit_servicio_id)
        consulta = consulta.filter_by(cit_servicio_id=cit_servicio.id)
    elif cit_servicio_clave is not None:
        cit_servicio = get_cit_servicio_with_clave(database, cit_servicio_clave)
        consulta = consulta.filter_by(cit_servicio_id=cit_servicio.id)

    # Filtrar por creado
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(CitCita.creado >= desde_dt).filter(CitCita.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0)
        consulta = consulta.filter(CitCita.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(CitCita.creado <= hasta_dt)

    # Filtrar por inicio
    if inicio is not None:
        desde_dt = datetime(year=inicio.year, month=inicio.month, day=inicio.day, hour=0, minute=0, second=0)
        hasta_dt = datetime(year=inicio.year, month=inicio.month, day=inicio.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(CitCita.inicio >= desde_dt).filter(CitCita.inicio <= hasta_dt)
    else:
        if inicio_desde is not None:
            desde_dt = datetime(year=inicio_desde.year, month=inicio_desde.month, day=inicio_desde.day, hour=0, minute=0, second=0)
            consulta = consulta.filter(CitCita.inicio >= desde_dt)
        if inicio_hasta is not None:
            hasta_dt = datetime(year=inicio_hasta.year, month=inicio_hasta.month, day=inicio_hasta.day, hour=23, minute=59, second=59)
            consulta = consulta.filter(CitCita.inicio <= hasta_dt)

    # Filtrar por estado
    if estado is not None:
        estado = safe_string(estado)
        if estado not in CitCita.ESTADOS:
            raise MyNotValidParamError("El estado no es válido")
        consulta = consulta.filter(CitCita.estado == estado)

    # Filtrar por oficina
    if oficina_id is not None:
        oficina = get_oficina(database, oficina_id)
        consulta = consulta.filter_by(oficina_id=oficina.id)
    elif oficina_clave is not None:
        oficina = get_oficina_with_clave(database, oficina_clave)
        consulta = consulta.filter_by(oficina_id=oficina.id)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(CitCita.id.desc())


def get_cit_cita(database: Session, cit_cita_id: int) -> CitCita:
    """Consultar una cita por su id"""
    cit_cita = database.query(CitCita).get(cit_cita_id)
    if cit_cita is None:
        raise MyNotExistsError("No existe ese cita")
    if cit_cita.estatus != "A":
        raise MyIsDeletedError("No es activo ese cita, está eliminado")
    return cit_cita


def get_cit_citas_agendadas_por_servicio_oficina(
    database: Session,
    inicio: date = None,
    inicio_desde: date = None,
    inicio_hasta: date = None,
    size: int = 100,
) -> Any:
    """Calcular las cantidades de citas agendadas por servicio y oficina"""

    # Consultar las columnas oficina clave, servicio clave y cantidad
    consulta = database.query(
        Oficina.clave.label("oficina"),
        CitServicio.clave.label("servicio"),
        count("*").label("cantidad"),
    )

    # Juntar las tablas de oficina y servicio
    consulta = consulta.select_from(CitCita).join(CitServicio, Oficina)

    # Filtrar estatus
    consulta = consulta.filter(CitCita.estatus == "A")
    consulta = consulta.filter(CitServicio.estatus == "A")
    consulta = consulta.filter(Oficina.estatus == "A")

    # Filtrar estados
    consulta = consulta.filter(or_(CitCita.estado == "ASISTIO", CitCita.estado == "PENDIENTE"))

    # Si no vienen inicio, inicio_desde, inicio_hasta, se usa el size como cantidad de dias
    if inicio is None and inicio_desde is None and inicio_hasta is None:
        hoy = date.today()
        inicio_desde = hoy - timedelta(days=size)
        inicio_hasta = hoy
    elif inicio is not None:
        if inicio_desde is not None:
            desde_dt = datetime(year=inicio_desde.year, month=inicio_desde.month, day=inicio_desde.day, hour=0, minute=0, second=0)
            consulta = consulta.filter(CitCita.inicio >= desde_dt)
        if inicio_hasta is not None:
            hasta_dt = datetime(year=inicio_hasta.year, month=inicio_hasta.month, day=inicio_hasta.day, hour=23, minute=59, second=59)
            consulta = consulta.filter(CitCita.inicio <= hasta_dt)

    # Agrupar por oficina y servicio y entregar
    return consulta.group_by(Oficina.clave, CitServicio.clave).order_by(Oficina.clave, CitServicio.clave)


def get_cit_citas_creados_por_dia(
    database: Session,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    size: int = 100,
) -> Any:
    """Consultar las cantidades de citas creadas por dia"""

    # Consultar las columnas creado y determinar la cantidad
    # Observe que para la columna `creado` se usa la función func.date()
    consulta = database.query(
        func.date(CitCita.creado).label("creado"),
        count(CitCita.id).label("cantidad"),
    )

    # Si no vienen creado, creado_desde, creado_hasta, se usa el size como cantidad de dias
    if creado is None and creado_desde is None and creado_hasta is None:
        hoy = date.today()
        creado_desde = hoy - timedelta(days=size)
        creado_hasta = hoy
    elif creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(CitCita.creado >= desde_dt).filter(CitCita.creado <= hasta_dt)
    else:
        if creado_desde is not None:
            desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0)
            consulta = consulta.filter(CitCita.creado >= desde_dt)
        if creado_hasta is not None:
            hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59)
            consulta = consulta.filter(CitCita.creado <= hasta_dt)

    # Agrupar por creado y entregar
    return consulta.group_by(func.date(CitCita.creado))


def get_cit_citas_creados_por_dia_distrito(
    database: Session,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    size: int = 100,
) -> Any:
    """Consultar las cantidades de citas creadas por dia y por distrito"""

    # Consultar las columnas creado, distrito y determinar la cantidad
    # Observe que para la columna `creado` se usa la función func.date()
    consulta = database.query(
        func.date(CitCita.creado).label("creado"),
        Distrito.nombre_corto.label("distrito"),
        count(CitCita.id).label("cantidad"),
    )

    # Juntar con oficinas y distritos
    consulta = consulta.select_from(CitCita).join(Oficina).join(Distrito)

    # Filtrar estados ASISTIO y PENDIENTE
    consulta = consulta.filter(or_(CitCita.estado == "ASISTIO", CitCita.estado == "PENDIENTE"))

    # Si no vienen creado, creado_desde, creado_hasta, se usa el size como cantidad de dias
    if creado is None and creado_desde is None and creado_hasta is None:
        hoy = date.today()
        creado_desde = hoy - timedelta(days=size)
        creado_hasta = hoy
    elif creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(CitCita.creado >= desde_dt).filter(CitCita.creado <= hasta_dt)
    else:
        if creado_desde is not None:
            desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0)
            consulta = consulta.filter(CitCita.creado >= desde_dt)
        if creado_hasta is not None:
            hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59)
            consulta = consulta.filter(CitCita.creado <= hasta_dt)

    # Agrupar por creado y por distrito
    consulta = consulta.group_by(func.date(CitCita.creado), Distrito.nombre_corto)

    # Ordenar y entregar
    return consulta.order_by(func.date(CitCita.creado), Distrito.nombre_corto)

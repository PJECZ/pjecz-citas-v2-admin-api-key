"""
Cit Citas v4, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_string

from ...core.cit_citas.models import CitCita
from ..cit_clientes.crud import get_cit_cliente, get_cit_cliente_with_curp, get_cit_cliente_with_email
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
    return consulta.filter_by(estatus="A").order_by(CitCita.id)


def get_cit_cita(database: Session, cit_cita_id: int) -> CitCita:
    """Consultar una cita por su id"""
    cit_cita = database.query(CitCita).get(cit_cita_id)
    if cit_cita is None:
        raise MyNotExistsError("No existe ese cita")
    if cit_cita.estatus != "A":
        raise MyIsDeletedError("No es activo ese cita, está eliminado")
    return cit_cita

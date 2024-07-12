"""
Cit Clientes Recuperaciones v4, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.cit_clientes_recuperaciones.models import CitClienteRecuperacion
from ..cit_clientes.crud import get_cit_cliente, get_cit_cliente_with_curp, get_cit_cliente_with_email


def get_cit_clientes_recuperaciones(
    database: Session,
    cit_cliente_id: int = None,
    cit_cliente_curp: str = None,
    cit_cliente_email: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    ya_recuperado: bool = None,
) -> Any:
    """Consultar las recuperaciones activas"""
    consulta = database.query(CitClienteRecuperacion)

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
        consulta = consulta.filter(CitClienteRecuperacion.creado >= desde_dt).filter(CitClienteRecuperacion.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0)
        consulta = consulta.filter(CitClienteRecuperacion.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(
            year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59
        )
        consulta = consulta.filter(CitClienteRecuperacion.creado <= hasta_dt)

    # Filtrar por ya recuperado
    if ya_recuperado is not None:
        consulta = consulta.filter(CitClienteRecuperacion.recuperado == ya_recuperado)

    # Entregar
    return consulta.filter(CitClienteRecuperacion.estatus == "A").order_by(CitClienteRecuperacion.id)


def get_cit_cliente_recuperacion(database: Session, cit_cliente_recuperacion_id: int) -> CitClienteRecuperacion:
    """Consultar una recuperacion por su id"""
    cit_cliente_recuperacion = database.query(CitClienteRecuperacion).get(cit_cliente_recuperacion_id)
    if cit_cliente_recuperacion is None:
        raise MyNotExistsError("No existe ese recuperacion")
    if cit_cliente_recuperacion.estatus != "A":
        raise MyIsDeletedError("No es activo ese recuperacion, está eliminado")
    return cit_cliente_recuperacion

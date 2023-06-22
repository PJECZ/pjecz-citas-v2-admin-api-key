"""
Cit Clientes Recuperaciones v3, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session
import pytz

from config.settings import Settings
from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_email

from ...core.cit_clientes_recuperaciones.models import CitClienteRecuperacion
from ..cit_clientes.crud import get_cit_cliente
from ..cit_clientes.models import CitCliente


def get_cit_clientes_recuperaciones(
    db: Session,
    settings: Settings,
    cit_cliente_id: int = None,
    cit_cliente_email: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    ya_recuperado: bool = None,
) -> Any:
    """Consultar las recuperaciones activas"""

    # Zonas horarias
    local_huso_horario = pytz.timezone(settings.tz)
    servidor_huso_horario = pytz.utc

    # Consultar
    consulta = db.query(CitClienteRecuperacion)

    # Filtrar por cliente
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(db, get_cit_cliente)
        consulta = consulta.filter(CitClienteRecuperacion.cit_cliente == cit_cliente)
    elif cit_cliente_email is not None:
        cit_cliente_email = safe_email(cit_cliente_email, search_fragment=False)
        if cit_cliente_email is None:
            raise MyNotValidParamError("No es válido el correo electrónico")
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.email == cit_cliente_email)

    # Filtrar por creado
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCliente.creado >= desde_dt).filter(CitCliente.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCliente.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCliente.creado <= hasta_dt)

    # Filtrar por ya recuperado
    if ya_recuperado is None:
        consulta = consulta.filter_by(ya_recuperado=False)  # Si no se especifica, se filtra por no recuperados
    else:
        consulta = consulta.filter_by(ya_recuperado=ya_recuperado)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(CitClienteRecuperacion.id)


def get_cit_cliente_recuperacion(db: Session, cit_cliente_recuperacion_id: int) -> CitClienteRecuperacion:
    """Consultar una recuperacion por su id"""
    cit_cliente_recuperacion = db.query(CitClienteRecuperacion).get(cit_cliente_recuperacion_id)
    if cit_cliente_recuperacion is None:
        raise MyNotExistsError("No existe ese recuperacion")
    if cit_cliente_recuperacion.estatus != "A":
        raise MyIsDeletedError("No es activo ese recuperacion, está eliminado")
    return cit_cliente_recuperacion

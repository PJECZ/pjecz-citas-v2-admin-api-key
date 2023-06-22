"""
Cit Clientes Registros v3, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any

from sqlalchemy.orm import Session
import pytz

from config.settings import Settings
from lib.exceptions import MyIsDeletedError, MyNotExistsError
from lib.safe_string import safe_curp, safe_email, safe_string

from ...core.cit_clientes_registros.models import CitClienteRegistro


def get_cit_clientes_registros(
    db: Session,
    settings: Settings,
    apellido_primero: str = None,
    apellido_segundo: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    curp: str = None,
    email: str = None,
    nombres: str = None,
    ya_registrado: bool = None,
) -> Any:
    """Consultar los registros de clientes activos"""
    consulta = db.query(CitClienteRegistro)

    # Zonas horarias
    local_huso_horario = pytz.timezone(settings.tz)
    servidor_huso_horario = pytz.utc

    # Consultar
    consulta = db.query(CitClienteRegistro)

    # Filtrar por apellido primero
    apellido_primero = safe_string(apellido_primero)
    if apellido_primero is not None:
        consulta = consulta.filter(CitClienteRegistro.apellido_primero.contains(apellido_primero))

    # Filtrar por apedillo segundo
    apellido_segundo = safe_string(apellido_segundo)
    if apellido_segundo is not None:
        consulta = consulta.filter(CitClienteRegistro.apellido_segundo.contains(apellido_segundo))

    # Filtrar por creado
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitClienteRegistro.creado >= desde_dt).filter(CitClienteRegistro.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitClienteRegistro.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitClienteRegistro.creado <= hasta_dt)

    # Filtrar por fragmento de CURP
    curp = safe_curp(curp, search_fragment=True)
    if curp is not None:
        consulta = consulta.filter(CitClienteRegistro.curp.contains(curp))

    # Filtrar por fragmento de email
    email = safe_email(email, search_fragment=True)
    if email is not None:
        consulta = consulta.filter(CitClienteRegistro.email.contains(email))

    # Filtrar por nombres
    nombres = safe_string(nombres)
    if nombres is not None:
        consulta = consulta.filter(CitClienteRegistro.nombres.contains(nombres))

    # Filtrar por ya registrado
    if ya_registrado is None:
        consulta = consulta.filter_by(ya_registrado=False)  # Si no se especifica, se filtra por no registrados
    else:
        consulta = consulta.filter_by(ya_registrado=ya_registrado)

    # Entregar
    return consulta.order_by(CitClienteRegistro.id.desc())


def get_cit_cliente_registro(db: Session, cit_cliente_registro_id: int) -> CitClienteRegistro:
    """Consultar un registro de cliente por su id"""
    cit_cliente_registro = db.query(CitClienteRegistro).get(cit_cliente_registro_id)
    if cit_cliente_registro is None:
        raise MyNotExistsError("No existe ese registro de cliente")
    if cit_cliente_registro.estatus != "A":
        raise MyIsDeletedError("No es activo ese registro de cliente, está eliminado")
    return cit_cliente_registro

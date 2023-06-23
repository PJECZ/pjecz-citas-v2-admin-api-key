"""
Cit Clientes v3, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session
import pytz

from config.settings import Settings
from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_curp, safe_email, safe_string, safe_telefono

from ...core.cit_clientes.models import CitCliente


def get_cit_clientes(
    db: Session,
    settings: Settings,
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

    # Zonas horarias
    local_huso_horario = pytz.timezone(settings.tz)
    servidor_huso_horario = pytz.utc

    # Consultar
    consulta = db.query(CitCliente)

    # Filtrar por apellido primero
    if apellido_primero is not None:
        apellido_primero = safe_string(apellido_primero)
        consulta = consulta.filter(CitCliente.apellido_primero.contains(apellido_primero))

    # Filtrar por apellido segundo
    if apellido_segundo is not None:
        apellido_segundo = safe_string(apellido_segundo)
        consulta = consulta.filter(CitCliente.apellido_segundo.contains(apellido_segundo))

    # Filtrar por autoriza mensajes
    if autoriza_mensajes is not None:
        consulta = consulta.filter(CitCliente.autoriza_mensajes == autoriza_mensajes)

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

    # Filtrar por fragmento de CURP
    if curp is not None:
        curp = safe_curp(curp, search_fragment=True)
        consulta = consulta.filter(CitCliente.curp.contains(curp))

    # Filtrar por fragmento de email
    if email is not None:
        email = safe_email(email, search_fragment=True)
        consulta = consulta.filter(CitCliente.email.contains(email))

    # Filtrar por enviar boletin
    if enviar_boletin is not None:
        consulta = consulta.filter(CitCliente.enviar_boletin == enviar_boletin)

    # Filtrar por nombres
    if nombres is not None:
        nombres = safe_string(nombres)
        consulta = consulta.filter(CitCliente.nombres.contains(nombres))

    # Filtrar por telefono
    if telefono is not None:
        telefono = safe_telefono(telefono)
        consulta = consulta.filter(CitCliente.telefono.contains(telefono))

    # Filtrar por contrasena sha256
    if tiene_contrasena_sha256 is not None:
        if tiene_contrasena_sha256:
            consulta = consulta.filter(CitCliente.contrasena_sha256 != "")
        else:
            consulta = consulta.filter(CitCliente.contrasena_sha256 == "")

    # Entregar
    return consulta.filter_by(estatus="A").order_by(CitCliente.id)


def get_cit_cliente(
    db: Session,
    cit_cliente_id: int = None,
    cit_cliente_curp: str = None,
    cit_cliente_email: str = None,
) -> CitCliente:
    """Consultar un cliente por su id"""
    if cit_cliente_id is not None:
        cit_cliente = db.query(CitCliente).get(cit_cliente_id)
    elif cit_cliente_curp is not None:
        curp = safe_curp(cit_cliente_curp, search_fragment=False)
        if curp is None:
            raise MyNotValidParamError("No es válido el CURP")
        cit_cliente = db.query(CitCliente).filter_by(curp=curp).first()
    elif cit_cliente_email is not None:
        email = safe_email(cit_cliente_email, search_fragment=False)
        if email is None:
            raise MyNotValidParamError("No es válido el correo electrónico")
        cit_cliente = db.query(CitCliente).filter_by(email=email).first()
    else:
        raise MyNotValidParamError("No se indicó el id, curp o email del cliente")
    if cit_cliente is None:
        raise MyNotExistsError("No existe ese cliente")
    if cit_cliente.estatus != "A":
        raise MyIsDeletedError("No es activo ese cliente, está eliminado")
    return cit_cliente

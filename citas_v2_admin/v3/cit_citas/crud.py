"""
Cit Citas v3, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, time, timedelta
from typing import Any

from sqlalchemy import or_
from sqlalchemy.orm import Session
import pytz

from config.settings import Settings
from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.pwgen import generar_codigo_asistencia
from lib.safe_string import safe_clave, safe_curp, safe_email, safe_string

from ...core.cit_citas.models import CitCita
from ...core.cit_clientes.models import CitCliente
from ...core.cit_servicios.models import CitServicio
from ...core.distritos.models import Distrito
from ...core.oficinas.models import Oficina
from ..cit_citas_anonimas.crud import get_cit_citas_anonimas
from ..cit_clientes.crud import get_cit_cliente
from ..cit_dias_disponibles.crud import get_cit_dias_disponibles
from ..cit_dias_inhabiles.crud import get_cit_dias_inhabiles
from ..cit_horas_disponibles.crud import get_cit_horas_disponibles
from ..cit_oficinas_servicios.crud import get_cit_oficinas_servicios
from ..cit_servicios.crud import get_cit_servicio
from ..distritos.crud import get_distrito
from ..oficinas.crud import get_oficina


def get_cit_citas(
    db: Session,
    settings: Settings,
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
    """Consultar las citas activos"""

    # Zonas horarias
    local_huso_horario = pytz.timezone(settings.tz)
    servidor_huso_horario = pytz.utc

    # Consultar
    consulta = db.query(CitCita)

    # Filtrar por cliente
    if cit_cliente_id is not None:
        cit_cliente = get_cit_cliente(db, cit_cliente_id)
        consulta = consulta.filter(CitCita.cit_cliente == cit_cliente)
    elif cit_cliente_curp is not None:
        cit_cliente_curp = safe_curp(cit_cliente_curp, search_fragment=False)
        if cit_cliente_curp is None:
            raise MyNotValidParamError("No es válido el CURP")
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.curp == cit_cliente_curp)
    elif cit_cliente_email is not None:
        cit_cliente_email = safe_email(cit_cliente_email, search_fragment=False)
        if cit_cliente_email is None:
            raise MyNotValidParamError("No es válido el correo electrónico")
        consulta = consulta.join(CitCliente)
        consulta = consulta.filter(CitCliente.email == cit_cliente_email)

    # Filtrar por servicio
    if cit_servicio_id is not None:
        cit_servicio = get_cit_servicio(db, cit_servicio_id)
        consulta = consulta.filter(CitCita.cit_servicio == cit_servicio)
    elif cit_servicio_clave is not None:
        cit_servicio_clave = safe_clave(cit_servicio_clave)
        if cit_servicio_clave is None:
            raise MyNotValidParamError("No es válida la clave del servicio")
        consulta = consulta.join(CitServicio)
        consulta = consulta.filter(CitServicio.clave == cit_servicio_clave)

    # Filtrar por creado
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCita.creado >= desde_dt).filter(CitCita.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCita.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCita.creado <= hasta_dt)

    # Filtrar por inicio
    if inicio is not None:
        desde_dt = datetime(year=inicio.year, month=inicio.month, day=inicio.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
        hasta_dt = datetime(year=inicio.year, month=inicio.month, day=inicio.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
        consulta = consulta.filter(CitCita.inicio >= desde_dt).filter(CitCita.inicio <= hasta_dt)
    else:
        if inicio_desde is not None:
            desde_dt = datetime(year=inicio_desde.year, month=inicio_desde.month, day=inicio_desde.day, hour=0, minute=0, second=0).astimezone(servidor_huso_horario)
            consulta = consulta.filter(CitCita.inicio >= desde_dt)
        if inicio_hasta is not None:
            hasta_dt = datetime(year=inicio_hasta.year, month=inicio_hasta.month, day=inicio_hasta.day, hour=23, minute=59, second=59).astimezone(servidor_huso_horario)
            consulta = consulta.filter(CitCita.inicio <= hasta_dt)

    # Filtrar por estado
    if estado is None:
        consulta = consulta.filter(or_(CitCita.estado == "ASISTIO", CitCita.estado == "PENDIENTE"))  # Si no se especifica, se filtra
    else:
        estado = safe_string(estado)
        if estado not in CitCita.ESTADOS:
            raise MyNotValidParamError("El estado no es válido")
        consulta = consulta.filter(CitCita.estado == estado)

    # Filtrar por oficina
    if oficina_id is not None:
        oficina = get_oficina(db, oficina_id)
        consulta = consulta.filter(CitCita.oficina == oficina)
    elif oficina_clave is not None:
        oficina_clave = safe_clave(oficina_clave)
        if oficina_clave is None:
            raise MyNotValidParamError("No es válida la clave de la oficina")
        consulta = consulta.join(Oficina)
        consulta = consulta.filter(Oficina.clave == oficina_clave)
    consulta = consulta.filter_by(estatus="A")

    # Entregar
    return consulta.filter_by(estatus="A").order_by(CitCita.id)


def get_cit_cita(db: Session, cit_cita_id: int) -> CitCita:
    """Consultar una cita por su id"""
    cit_cita = db.query(CitCita).get(cit_cita_id)
    if cit_cita is None:
        raise MyNotExistsError("No existe ese cita")
    if cit_cita.estatus != "A":
        raise MyIsDeletedError("No es activo ese cita, está eliminado")
    return cit_cita

"""
Cit Citas v4, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, time, timedelta
from typing import Any

from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import count, func

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.pwgen import generar_codigo_asistencia
from lib.safe_string import safe_string

from ...core.cit_citas.models import CitCita
from ...core.cit_servicios.models import CitServicio
from ...core.distritos.models import Distrito
from ...core.oficinas.models import Oficina
from ..cit_citas_anonimas.crud import get_cit_citas_anonimas
from ..cit_clientes.crud import get_cit_cliente, get_cit_cliente_with_curp, get_cit_cliente_with_email
from ..cit_dias_disponibles.crud import get_cit_dias_disponibles
from ..cit_dias_inhabiles.crud import get_cit_dias_inhabiles
from ..cit_horas_disponibles.crud import get_cit_horas_disponibles
from ..cit_oficinas_servicios.crud import get_cit_oficinas_servicios
from ..cit_servicios.crud import get_cit_servicio, get_cit_servicio_with_clave
from ..oficinas.crud import get_oficina, get_oficina_with_clave

LIMITE_CITAS_PENDIENTES = 30


def get_cit_cita(database: Session, cit_cita_id: int) -> CitCita:
    """Consultar una cita por su id"""
    cit_cita = database.query(CitCita).get(cit_cita_id)
    if cit_cita is None:
        raise MyNotExistsError("No existe ese cita")
    if cit_cita.estatus != "A":
        raise MyIsDeletedError("No es activo ese cita, está eliminado")
    return cit_cita


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
        hasta_dt = datetime(
            year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59
        )
        consulta = consulta.filter(CitCita.creado <= hasta_dt)

    # Filtrar por inicio
    if inicio is not None:
        desde_dt = datetime(year=inicio.year, month=inicio.month, day=inicio.day, hour=0, minute=0, second=0)
        hasta_dt = datetime(year=inicio.year, month=inicio.month, day=inicio.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(CitCita.inicio >= desde_dt).filter(CitCita.inicio <= hasta_dt)
    else:
        if inicio_desde is not None:
            desde_dt = datetime(
                year=inicio_desde.year, month=inicio_desde.month, day=inicio_desde.day, hour=0, minute=0, second=0
            )
            consulta = consulta.filter(CitCita.inicio >= desde_dt)
        if inicio_hasta is not None:
            hasta_dt = datetime(
                year=inicio_hasta.year, month=inicio_hasta.month, day=inicio_hasta.day, hour=23, minute=59, second=59
            )
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
    return consulta.filter(CitCita.estatus == "A").order_by(CitCita.id.desc())


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
            desde_dt = datetime(
                year=inicio_desde.year, month=inicio_desde.month, day=inicio_desde.day, hour=0, minute=0, second=0
            )
            consulta = consulta.filter(CitCita.inicio >= desde_dt)
        if inicio_hasta is not None:
            hasta_dt = datetime(
                year=inicio_hasta.year, month=inicio_hasta.month, day=inicio_hasta.day, hour=23, minute=59, second=59
            )
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
            desde_dt = datetime(
                year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0
            )
            consulta = consulta.filter(CitCita.creado >= desde_dt)
        if creado_hasta is not None:
            hasta_dt = datetime(
                year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59
            )
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
            desde_dt = datetime(
                year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0
            )
            consulta = consulta.filter(CitCita.creado >= desde_dt)
        if creado_hasta is not None:
            hasta_dt = datetime(
                year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59
            )
            consulta = consulta.filter(CitCita.creado <= hasta_dt)

    # Agrupar por creado y por distrito
    consulta = consulta.group_by(func.date(CitCita.creado), Distrito.nombre_corto)

    # Ordenar y entregar
    return consulta.order_by(func.date(CitCita.creado), Distrito.nombre_corto)


def get_cit_citas_disponibles_cantidad(
    database: Session,
    cit_cliente_id: int,
) -> int:
    """Consultar la cantidad de citas que puede agendar (que es su limite menos las pendientes)"""

    # Consultar cliente
    cit_cliente = get_cit_cliente(
        database=database,
        cit_cliente_id=cit_cliente_id,
    )

    # Definir la cantidad limite de citas del cliente
    limite = LIMITE_CITAS_PENDIENTES
    if cit_cliente.limite_citas_pendientes > limite:
        limite = cit_cliente.limite_citas_pendientes

    # Consultar la cantidad de citas PENDIENTES del cliente
    citas_pendientes_cantidad = get_cit_citas(
        database=database,
        cit_cliente_id=cit_cliente_id,
        estado="PENDIENTE",
        inicio_desde=date.today(),
    ).count()

    # Si la cantidad de citas pendientes es mayor o igual al limite, no puede agendar
    if citas_pendientes_cantidad >= limite:
        return 0

    # De lo contrario, puede agendar
    return limite - citas_pendientes_cantidad


def create_cit_cita(
    database: Session,
    cit_cliente_id: int,
    cit_servicio_id: int,
    fecha: date,
    hora_minuto: time,
    oficina_id: int,
    notas: str,
) -> CitCita:
    """Crear una cita"""

    # Consultar el cliente
    cit_cliente = get_cit_cliente(database=database, cit_cliente_id=cit_cliente_id)

    # Consultar la oficina
    oficina = get_oficina(database=database, oficina_id=oficina_id)

    # Consultar el servicio
    cit_servicio = get_cit_servicio(database=database, cit_servicio_id=cit_servicio_id)

    # Validar que ese servicio lo ofrezca esta oficina
    cit_oficinas_servicios = get_cit_oficinas_servicios(database=database, oficina_id=oficina_id).all()
    if cit_servicio_id not in [cit_oficina_servicio.cit_servicio_id for cit_oficina_servicio in cit_oficinas_servicios]:
        raise MyNotValidParamError("No es posible agendar este servicio en esta oficina")

    # Validar la fecha, debe ser un dia disponible
    if fecha not in get_cit_dias_disponibles(database=database):
        raise MyNotValidParamError("No es valida la fecha")

    # Validar la hora_minuto, respecto a las horas disponibles
    if hora_minuto not in get_cit_horas_disponibles(
        database=database, cit_servicio_id=cit_servicio_id, fecha=fecha, oficina_id=oficina_id
    ):
        raise MyNotValidParamError("No es valida la hora-minuto porque no esta disponible")

    # Validar que las citas en ese tiempo para esa oficina NO hayan llegado al limite de personas
    cit_citas_anonimas = get_cit_citas_anonimas(database=database, fecha=fecha, hora_minuto=hora_minuto, oficina_id=oficina_id)
    if cit_citas_anonimas.count() >= oficina.limite_personas:
        raise MyNotValidParamError("No se puede crear la cita porque ya se alcanzo el limite de personas en la oficina")

    # Validar que la cantidad de citas con estado PENDIENTE no haya llegado al limite de este cliente
    if get_cit_citas_disponibles_cantidad(database=database, cit_cliente_id=cit_cliente.id) <= 0:
        raise MyNotValidParamError("No se puede crear la cita porque ya se alcanzo el limite de citas pendientes")

    # Definir los tiempos de la cita
    inicio_dt = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=hora_minuto.hour, minute=hora_minuto.minute)
    termino_dt = datetime(
        year=fecha.year, month=fecha.month, day=fecha.day, hour=hora_minuto.hour, minute=hora_minuto.minute
    ) + timedelta(hours=cit_servicio.duracion.hour, minutes=cit_servicio.duracion.minute)

    # Validar que no tenga una cita pendiente en la misma fecha y hora
    cit_citas = get_cit_citas(database=database, cit_cliente_id=cit_cliente_id, estado="PENDIENTE")
    for cit_cita in cit_citas.all():
        if cit_cita.inicio == inicio_dt:
            raise MyNotValidParamError("No se puede crear la cita porque ya tiene una pendiente en la misma fecha y hora")

    # Definir cancelar_antes con 24 horas antes de la cita
    cancelar_antes = inicio_dt - timedelta(hours=24)

    # Si cancelar_antes es un dia inhabil, domingo o sabado, se busca el dia habil anterior
    dias_inhabiles = get_cit_dias_inhabiles(database=database).all()
    while cancelar_antes.date() in dias_inhabiles or cancelar_antes.weekday() == 6 or cancelar_antes.weekday() == 5:
        if cancelar_antes.date() in dias_inhabiles:
            cancelar_antes = cancelar_antes - timedelta(days=1)
        if cancelar_antes.weekday() == 6:  # Si es domingo, se cambia a viernes
            cancelar_antes = cancelar_antes - timedelta(days=2)
        if cancelar_antes.weekday() == 5:  # Si es sábado, se cambia a viernes
            cancelar_antes = cancelar_antes - timedelta(days=1)

    # Insertar registro
    cit_cita = CitCita(
        cit_servicio_id=cit_servicio.id,
        cit_cliente_id=cit_cliente_id,
        oficina_id=oficina.id,
        inicio=inicio_dt,
        termino=termino_dt,
        notas=safe_string(input_str=notas, max_len=512),
        estado="PENDIENTE",
        asistencia=False,
        codigo_asistencia=generar_codigo_asistencia(),
        cancelar_antes=cancelar_antes,
    )
    database.add(cit_cita)
    database.commit()
    database.refresh(cit_cita)

    # Entregar
    return cit_cita


def cancel_cit_cita(
    database: Session,
    cit_cita_id: int,
    cit_cliente_id: int,
) -> Any:
    """Cancelar una cita de un cliente"""

    # Consultar la cita
    cit_cita = get_cit_cita(database=database, cit_cita_id=cit_cita_id)

    # Validar que la cita sea del cliente
    if cit_cita.cit_cliente_id != cit_cliente_id:
        raise MyNotValidParamError("La cita no es de Usted")

    # Validar que no este cancelada
    if cit_cita.estado == "CANCELO":
        raise MyNotValidParamError("Ya esta cancelada esta cita")

    # Validar que se pueda cancelar
    if cit_cita.puede_cancelarse is False:
        raise MyNotValidParamError("No se puede cancelar esta cita")

    # Actualizar registro
    cit_cita.estado = "CANCELO"
    database.add(cit_cita)
    database.commit()
    database.refresh(cit_cita)

    # Entregar
    return cit_cita

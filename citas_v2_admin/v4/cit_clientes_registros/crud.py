"""
Cit Clientes Registros v4, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_curp, safe_email, safe_string, safe_telefono

from ...core.cit_clientes_registros.models import CitClienteRegistro


def get_cit_clientes_registros(
    database: Session,
    apellido_primero: str = None,
    apellido_segundo: str = None,
    creado: date = None,
    creado_desde: date = None,
    creado_hasta: date = None,
    curp: str = None,
    email: str = None,
    nombres: str = None,
    telefono: str = None,
    ya_registrado: bool = None,
) -> Any:
    """Consultar los registros de los clientes activos"""
    consulta = database.query(CitClienteRegistro)

    # Filtrar por apellido primero
    if apellido_primero is not None:
        apellido_primero = safe_string(apellido_primero)
        if apellido_primero != "":
            consulta = consulta.filter(CitClienteRegistro.apellido_primero.contains(apellido_primero))

    # Filtrar por apellido segundo
    if apellido_segundo is not None:
        apellido_segundo = safe_string(apellido_segundo)
        if apellido_segundo != "":
            consulta = consulta.filter(CitClienteRegistro.apellido_segundo.contains(apellido_segundo))

    # Filtrar por creado
    if creado is not None:
        desde_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=0, minute=0, second=0)
        hasta_dt = datetime(year=creado.year, month=creado.month, day=creado.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(CitClienteRegistro.creado >= desde_dt).filter(CitClienteRegistro.creado <= hasta_dt)
    if creado is None and creado_desde is not None:
        desde_dt = datetime(year=creado_desde.year, month=creado_desde.month, day=creado_desde.day, hour=0, minute=0, second=0)
        consulta = consulta.filter(CitClienteRegistro.creado >= desde_dt)
    if creado is None and creado_hasta is not None:
        hasta_dt = datetime(year=creado_hasta.year, month=creado_hasta.month, day=creado_hasta.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(CitClienteRegistro.creado <= hasta_dt)

    # Filtrar por fragmento de CURP
    if curp is not None:
        try:
            curp = safe_curp(curp, search_fragment=True)
        except ValueError as error:
            raise MyNotValidParamError("No es un CURP válido") from error
        consulta = consulta.filter(CitClienteRegistro.curp.contains(curp))

    # Filtrar por fragmento de email
    if email is not None:
        try:
            email = safe_email(email, search_fragment=True)
        except ValueError as error:
            raise MyNotValidParamError("No es un email válido") from error
        consulta = consulta.filter(CitClienteRegistro.email.contains(email))

    # Filtrar por nombres
    if nombres is not None:
        nombres = safe_string(nombres)
        if nombres != "":
            consulta = consulta.filter(CitClienteRegistro.nombres.contains(nombres))

    # Filtrar por telefono
    if telefono is not None:
        try:
            telefono = safe_telefono(telefono)
        except ValueError as error:
            raise MyNotValidParamError("No es un telefono válido") from error
        consulta = consulta.filter(CitClienteRegistro.telefono.contains(telefono))

    # Filtrar por ya registrado
    if ya_registrado is not None:
        consulta = consulta.filter(CitClienteRegistro.ya_registrado == ya_registrado)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(CitClienteRegistro.id)


def get_cit_cliente_registro(database: Session, cit_cliente_registro_id: int) -> CitClienteRegistro:
    """Consultar un registro de cliente por su id"""
    cit_cliente_registro = database.query(CitClienteRegistro).get(cit_cliente_registro_id)
    if cit_cliente_registro is None:
        raise MyNotExistsError("No existe ese registro de cliente")
    if cit_cliente_registro.estatus != "A":
        raise MyIsDeletedError("No es activo ese registro de cliente, está eliminado")
    return cit_cliente_registro

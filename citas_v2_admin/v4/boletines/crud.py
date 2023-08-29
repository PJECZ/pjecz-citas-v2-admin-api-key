"""
Boletines v4, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_string

from ...core.boletines.models import Boletin


def get_boletines(
    database: Session,
    estado: str = None,
    envio_programado_desde: date = None,
    envio_programado_hasta: date = None,
) -> Any:
    """Consultar los boletines activos"""
    consulta = database.query(Boletin)
    if estado is not None:
        estado = safe_string(estado)
        if estado not in Boletin.ESTADOS:
            raise MyNotValidParamError("No es un estado válido")
        consulta = consulta.filter_by(estado=estado)
    if envio_programado_desde is not None:
        consulta = consulta.filter(Boletin.envio_programado >= envio_programado_desde)
    if envio_programado_hasta is not None:
        consulta = consulta.filter(Boletin.envio_programado <= envio_programado_hasta)
    return consulta.filter_by(estatus="A").order_by(Boletin.envio_programado)


def get_boletin(database: Session, boletin_id: int) -> Boletin:
    """Consultar un boletin por su id"""
    boletin = database.query(Boletin).get(boletin_id)
    if boletin is None:
        raise MyNotExistsError("No existe ese boletin")
    if boletin.estatus != "A":
        raise MyIsDeletedError("No es activo ese boletin, está eliminado")
    return boletin

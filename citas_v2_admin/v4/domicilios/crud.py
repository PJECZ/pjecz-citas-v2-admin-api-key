"""
Domicilios v4, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.domicilios.models import Domicilio
from ..distritos.crud import get_distrito, get_distrito_with_clave


def get_domicilios(
    database: Session,
    distrito_id: int = None,
    distrito_clave: str = None,
) -> Any:
    """Consultar los domicilios activos"""
    consulta = database.query(Domicilio)
    if distrito_id is not None:
        distrito = get_distrito(database, distrito_id)
        consulta = consulta.filter_by(distrito_id=distrito.id)
    elif distrito_clave is not None:
        distrito = get_distrito_with_clave(database, distrito_clave)
        consulta = consulta.filter_by(distrito_id=distrito.id)
    return consulta.filter(Domicilio.estatus == "A").order_by(Domicilio.id)


def get_domicilio(database: Session, domicilio_id: int) -> Domicilio:
    """Consultar un domicilio por su id"""
    domicilio = database.query(Domicilio).get(domicilio_id)
    if domicilio is None:
        raise MyNotExistsError("No existe ese domicilio")
    if domicilio.estatus != "A":
        raise MyIsDeletedError("No es activo ese domicilio, está eliminado")
    return domicilio

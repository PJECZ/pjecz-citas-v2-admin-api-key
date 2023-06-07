"""
Distritos v3, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_clave

from ...core.distritos.models import Distrito


def get_distritos(
    db: Session,
    es_distrito_judicial: bool = None,
    es_distrito: bool = None,
    es_jurisdiccional: bool = None,
) -> Any:
    """Consultar los distritos activos"""
    consulta = db.query(Distrito)
    if es_distrito_judicial is not None:
        consulta = consulta.filter_by(es_distrito_judicial=es_distrito_judicial)
    if es_distrito is not None:
        consulta = consulta.filter_by(es_distrito=es_distrito)
    if es_jurisdiccional is not None:
        consulta = consulta.filter_by(es_jurisdiccional=es_jurisdiccional)
    return consulta.filter_by(estatus="A").order_by(Distrito.clave)


def get_distrito(db: Session, distrito_id: int) -> Distrito:
    """Consultar un distrito por su id"""
    distrito = db.query(Distrito).get(distrito_id)
    if distrito is None:
        raise MyNotExistsError("No existe ese distrito")
    if distrito.estatus != "A":
        raise MyIsDeletedError("No es activo ese distrito, está eliminado")
    return distrito


def get_distrito_with_clave(db: Session, distrito_clave: str) -> Distrito:
    """Consultar un distrito por su clave"""
    try:
        clave = safe_clave(distrito_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    distrito = db.query(Distrito).filter_by(clave=clave).first()
    if distrito is None:
        raise MyNotExistsError("No existe ese distrito")
    if distrito.estatus != "A":
        raise MyIsDeletedError("No es activo ese distrito, está eliminado")
    return distrito

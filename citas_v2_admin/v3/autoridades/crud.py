"""
Autoridades v3, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_clave

from ...core.autoridades.models import Autoridad
from ..distritos.crud import get_distrito, get_distrito_with_clave
from ..materias.crud import get_materia, get_materia_with_clave


def get_autoridades(
    db: Session,
    distrito_id: int = None,
    distrito_clave: str = None,
    es_jurisdiccional: bool = None,
    es_notaria: bool = None,
    es_organo_especializado: bool = None,
    materia_id: int = None,
    materia_clave: str = None,
) -> Any:
    """Consultar los autoridades activos"""
    consulta = db.query(Autoridad)
    if distrito_id is not None:
        distrito = get_distrito(db, distrito_id)
        consulta = consulta.filter_by(distrito_id=distrito.id)
    elif distrito_clave is not None:
        distrito = get_distrito_with_clave(db, distrito_clave)
        consulta = consulta.filter_by(distrito_id=distrito.id)
    if es_jurisdiccional is not None:
        consulta = consulta.filter_by(es_jurisdiccional=es_jurisdiccional)
    if es_notaria is not None:
        consulta = consulta.filter_by(es_notaria=es_notaria)
    if es_organo_especializado is not None:
        consulta = consulta.filter_by(es_organo_especializado=es_organo_especializado)
    if materia_id is not None:
        materia = get_materia(db, materia_id)
        consulta = consulta.filter_by(materia_id=materia.id)
    elif materia_clave is not None:
        materia = get_materia_with_clave(db, materia_clave)
        consulta = consulta.filter_by(materia_id=materia.id)
    return consulta.filter_by(estatus="A").order_by(Autoridad.id)


def get_autoridad(db: Session, autoridad_id: int) -> Autoridad:
    """Consultar un autoridad por su id"""
    autoridad = db.query(Autoridad).get(autoridad_id)
    if autoridad is None:
        raise MyNotExistsError("No existe ese autoridad")
    if autoridad.estatus != "A":
        raise MyIsDeletedError("No es activo ese autoridad, está eliminado")
    return autoridad


def get_autoridad_with_clave(db: Session, autoridad_clave: str) -> Autoridad:
    """Consultar un autoridad por su clave"""
    try:
        clave = safe_clave(autoridad_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    autoridad = db.query(Autoridad).filter_by(clave=clave).first()
    if autoridad is None:
        raise MyNotExistsError("No existe ese autoridad")
    if autoridad.estatus != "A":
        raise MyIsDeletedError("No es activo ese autoridad, está eliminado")
    return autoridad

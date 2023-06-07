"""
Materias v3, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_clave

from ...core.materias.models import Materia


def get_materias(db: Session) -> Any:
    """Consultar los materias activos"""
    return db.query(Materia).filter_by(estatus="A").order_by(Materia.id)


def get_materia(db: Session, materia_id: int) -> Materia:
    """Consultar un materia por su id"""
    materia = db.query(Materia).get(materia_id)
    if materia is None:
        raise MyNotExistsError("No existe ese materia")
    if materia.estatus != "A":
        raise MyIsDeletedError("No es activo ese materia, está eliminado")
    return materia


def get_materia_with_clave(db: Session, materia_clave: str) -> Materia:
    """Consultar un materia por su clave"""
    try:
        clave = safe_clave(materia_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    materia = db.query(Materia).filter_by(clave=clave).first()
    if materia is None:
        raise MyNotExistsError("No existe ese materia")
    if materia.estatus != "A":
        raise MyIsDeletedError("No es activo ese materia, está eliminado")
    return materia

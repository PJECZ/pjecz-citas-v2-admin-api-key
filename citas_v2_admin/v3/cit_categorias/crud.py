"""
Cit Categorias v3, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.cit_categorias.models import CitCategoria


def get_cit_categorias(db: Session) -> Any:
    """Consultar los categorias activos"""
    return db.query(CitCategoria).filter_by(estatus="A").order_by(CitCategoria.nombre)


def get_cit_categoria(db: Session, cit_categoria_id: int) -> CitCategoria:
    """Consultar un categoria por su id"""
    cit_categoria = db.query(CitCategoria).get(cit_categoria_id)
    if cit_categoria is None:
        raise MyNotExistsError("No existe ese categoria")
    if cit_categoria.estatus != "A":
        raise MyIsDeletedError("No es activo ese categoria, está eliminado")
    return cit_categoria

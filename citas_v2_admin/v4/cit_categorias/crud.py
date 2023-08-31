"""
Cit Categorias v4, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.cit_categorias.models import CitCategoria


def get_cit_categorias(database: Session) -> Any:
    """Consultar las categorias activas"""
    return database.query(CitCategoria).filter_by(estatus="A").order_by(CitCategoria.nombre)


def get_cit_categoria(database: Session, cit_categoria_id: int) -> CitCategoria:
    """Consultar una categoria por su id"""
    cit_categoria = database.query(CitCategoria).get(cit_categoria_id)
    if cit_categoria is None:
        raise MyNotExistsError("No existe ese categoria")
    if cit_categoria.estatus != "A":
        raise MyIsDeletedError("No es activo ese categoria, está eliminado")
    return cit_categoria

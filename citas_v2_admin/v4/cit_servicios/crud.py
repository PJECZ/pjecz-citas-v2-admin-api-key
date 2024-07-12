"""
Cit Servicios v4, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.cit_servicios.models import CitServicio
from ..cit_categorias.crud import get_cit_categoria


def get_cit_servicios(
    database: Session,
    cit_categoria_id: int = None,
) -> Any:
    """Consultar los servicios activos"""
    consulta = database.query(CitServicio)
    if cit_categoria_id is not None:
        cit_categoria = get_cit_categoria(database, cit_categoria_id)
        consulta = consulta.filter_by(cit_categoria=cit_categoria)
    return consulta.filter(CitServicio.estatus == "A").order_by(CitServicio.id)


def get_cit_servicio(database: Session, cit_servicio_id: int) -> CitServicio:
    """Consultar un servicio por su id"""
    cit_servicio = database.query(CitServicio).get(cit_servicio_id)
    if cit_servicio is None:
        raise MyNotExistsError("No existe ese servicio")
    if cit_servicio.estatus != "A":
        raise MyIsDeletedError("No es activo ese servicio, está eliminado")
    return cit_servicio


def get_cit_servicio_with_clave(database: Session, cit_servicio_clave: str) -> CitServicio:
    """Consultar un servicio por su clave"""
    cit_servicio = database.query(CitServicio).filter_by(clave=cit_servicio_clave).first()
    if cit_servicio is None:
        raise MyNotExistsError("No existe ese servicio")
    if cit_servicio.estatus != "A":
        raise MyIsDeletedError("No es activo ese servicio, está eliminado")
    return cit_servicio

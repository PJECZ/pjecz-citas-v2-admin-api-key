"""
Cit Oficinas-Servicios v4, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.cit_oficinas_servicios.models import CitOficinaServicio
from ..cit_servicios.crud import get_cit_servicio, get_cit_servicio_with_clave
from ..oficinas.crud import get_oficina, get_oficina_with_clave


def get_cit_oficinas_servicios(
    database: Session,
    cit_servicio_id: int = None,
    cit_servicio_clave: str = None,
    oficina_id: int = None,
    oficina_clave: str = None,
) -> Any:
    """Consultar los oficinas-servicios activos"""
    consulta = database.query(CitOficinaServicio)
    if cit_servicio_id is not None:
        cit_servicio = get_cit_servicio(database, cit_servicio_id)
        consulta = consulta.filter_by(cit_servicio=cit_servicio)
    elif cit_servicio_clave is not None:
        cit_servicio = get_cit_servicio_with_clave(database, cit_servicio_clave)
        consulta = consulta.filter_by(cit_servicio=cit_servicio)
    if oficina_id is not None:
        oficina = get_oficina(database, oficina_id)
        consulta = consulta.filter_by(oficina=oficina)
    elif oficina_clave is not None:
        oficina = get_oficina_with_clave(database, oficina_clave)
        consulta = consulta.filter_by(oficina=oficina)
    return consulta.filter_by(estatus="A").order_by(CitOficinaServicio.id)


def get_oficina_servicio(database: Session, oficina_servicio_id: int) -> CitOficinaServicio:
    """Consultar un oficina-servicio por su id"""
    oficina_servicio = database.query(CitOficinaServicio).get(oficina_servicio_id)
    if oficina_servicio is None:
        raise MyNotExistsError("No existe ese oficina-servicio")
    if oficina_servicio.estatus != "A":
        raise MyIsDeletedError("No es activo ese oficina-servicio, está eliminado")
    return oficina_servicio

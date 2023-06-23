"""
Cit Oficinas-Servicios v3, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.cit_oficinas_servicios.models import CitOficinaServicio
from ..cit_servicios.crud import get_cit_servicio
from ..oficinas.crud import get_oficina


def get_cit_oficinas_servicios(
    db: Session,
    cit_servicio_id: int = None,
    oficina_id: int = None,
) -> Any:
    """Consultar las oficinas-servicios activas"""
    consulta = db.query(CitOficinaServicio)
    if cit_servicio_id is not None:
        cit_servicio = get_cit_servicio(db, cit_servicio_id)
        consulta = consulta.filter(CitOficinaServicio.cit_servicio == cit_servicio)
    if oficina_id is not None:
        oficina = get_oficina(db, oficina_id)
        consulta = consulta.filter(CitOficinaServicio.oficina == oficina)
    return consulta.filter_by(estatus="A").order_by(CitOficinaServicio.id)


def get_cit_oficina_servicio(db: Session, oficina_servicio_id: int) -> CitOficinaServicio:
    """Consultar una oficina-servicio por su id"""
    oficina_servicio = db.query(CitOficinaServicio).get(oficina_servicio_id)
    if oficina_servicio is None:
        raise MyNotExistsError("No existe ese oficina-servicio")
    if oficina_servicio.estatus != "A":
        raise MyIsDeletedError("No es activo ese oficina-servicio, está eliminado")
    return oficina_servicio

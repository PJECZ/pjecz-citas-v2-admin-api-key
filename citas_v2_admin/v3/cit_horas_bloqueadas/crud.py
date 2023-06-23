"""
Cit Horas Bloqueadas v3, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.cit_horas_bloqueadas.models import CitHoraBloqueada
from ..oficinas.crud import get_oficina


def get_cit_horas_bloqueadas(
    db: Session,
    fecha: date = None,
    oficina_id: int = None,
) -> Any:
    """Consultar los horas bloqueadas activos"""
    consulta = db.query(CitHoraBloqueada)
    if fecha is not None:
        consulta = consulta.filter_by(fecha=fecha)
    if oficina_id is not None:
        oficina = get_oficina(db, oficina_id)
        consulta = consulta.filter(CitHoraBloqueada.oficina == oficina)
    consulta = consulta.filter(CitHoraBloqueada.fecha >= date.today())  # Solo los dias de hoy en adelante
    return consulta.filter_by(estatus="A").order_by(CitHoraBloqueada.id)


def get_cit_hora_bloqueada(db: Session, cit_hora_bloqueada_id: int) -> CitHoraBloqueada:
    """Consultar un hora bloqueada por su id"""
    cit_hora_bloqueada = db.query(CitHoraBloqueada).get(cit_hora_bloqueada_id)
    if cit_hora_bloqueada is None:
        raise MyNotExistsError("No existe ese hora bloqueada")
    if cit_hora_bloqueada.estatus != "A":
        raise MyIsDeletedError("No es activo ese hora bloqueada, está eliminado")
    return cit_hora_bloqueada

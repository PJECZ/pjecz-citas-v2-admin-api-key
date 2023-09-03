"""
Cit Horas Bloqueadas v4, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.cit_horas_bloqueadas.models import CitHoraBloqueada
from ..oficinas.crud import get_oficina


def get_cit_horas_bloqueadas(
    database: Session,
    fecha: date,
    oficina_id: int,
) -> Any:
    """Consultar las horas bloqueadas activas"""
    consulta = database.query(CitHoraBloqueada)

    # Filtrar por fecha
    consulta = consulta.filter_by(fecha=fecha)

    # Filtrar por oficina
    oficina = get_oficina(database, oficina_id)
    consulta = consulta.filter_by(oficina=oficina)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(CitHoraBloqueada.id.desc())


def get_cit_hora_bloqueada(database: Session, cit_hora_bloqueada_id: int) -> CitHoraBloqueada:
    """Consultar una hora bloqueada por su id"""
    cit_hora_bloqueada = database.query(CitHoraBloqueada).get(cit_hora_bloqueada_id)
    if cit_hora_bloqueada is None:
        raise MyNotExistsError("No existe ese hora bloqueada")
    if cit_hora_bloqueada.estatus != "A":
        raise MyIsDeletedError("No es activo ese hora bloqueada, está eliminado")
    return cit_hora_bloqueada

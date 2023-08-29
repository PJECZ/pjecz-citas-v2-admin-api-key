"""
Cit Citas Anonimas v4, CRUD (create, read, update, and delete)
"""
from datetime import date, time
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.cit_citas.models import CitCita


def get_cit_citas_anonimas(
    database: Session,
    oficina_id: int,
    fecha: date = None,
    hora_minuto: time = None,
) -> Any:
    """Consultar los citas de forma anonima, esto sirve para saber si hay citas disponibles en una oficina en un dia y hora especifica"""
    consulta = database.query(CitCita)
    return consulta.filter_by(estatus="A").order_by(CitCita.id)

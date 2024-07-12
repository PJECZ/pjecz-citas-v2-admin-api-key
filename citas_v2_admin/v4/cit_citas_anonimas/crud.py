"""
Cit Citas Anonimas v4, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, time
from typing import Any

from sqlalchemy.orm import Session

from ...core.cit_citas.models import CitCita
from ..oficinas.crud import get_oficina


def get_cit_citas_anonimas(
    database: Session,
    fecha: date,
    oficina_id: int,
    hora_minuto: time = None,
) -> Any:
    """Consultar los citas de forma anonima, esto sirve para saber si hay citas disponibles en una oficina en un dia y hora especifica"""
    consulta = database.query(CitCita)

    # Si viene hora_minuto
    if fecha is not None and hora_minuto is not None:
        inicio_dt = datetime(
            year=fecha.year, month=fecha.month, day=fecha.day, hour=hora_minuto.hour, minute=hora_minuto.minute, second=0
        )
        consulta = consulta.filter(CitCita.inicio == inicio_dt)
    else:
        # Se filtra por fecha
        inicio_dt = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=0, minute=0, second=0)
        termino_dt = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=23, minute=59, second=59)
        consulta = consulta.filter(CitCita.inicio >= inicio_dt).filter(CitCita.inicio <= termino_dt)

    # Filtrar por oficina
    oficina = get_oficina(database, oficina_id)
    consulta = consulta.filter_by(oficina_id=oficina.id)

    # Descartar las citas canceladas
    consulta = consulta.filter(CitCita.estado != "CANCELO")

    # Entregar
    return consulta.filter(CitCita.estatus == "A").order_by(CitCita.id.desc())

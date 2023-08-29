"""
Cit Horas Disponibles v4, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from ..cit_citas_anonimas.crud import get_cit_citas_anonimas
from ..cit_dias_disponibles.crud import get_cit_dias_disponibles
from ..cit_horas_bloqueadas.crud import get_cit_horas_bloqueadas
from ..cit_servicios.crud import get_cit_servicio, get_cit_servicio_with_clave
from ..oficinas.crud import get_oficina, get_oficina_with_clave


def get_cit_horas_disponibles(
    database: Session,
    cit_servicio_id: int,
    cit_servicio_clave: str,
    fecha: date,
    oficina_id: int,
    oficina_clave: str,
    size: int = 100,
) -> Any:
    """Consultar los horas disponibles activos"""
    listado = []
    return listado

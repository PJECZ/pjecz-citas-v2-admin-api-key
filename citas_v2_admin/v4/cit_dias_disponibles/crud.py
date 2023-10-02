"""
Cit Dias Disponibles v4, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import List

import pytz
from sqlalchemy.orm import Session

from ..cit_dias_inhabiles.crud import get_cit_dias_inhabiles

LIMITE_DIAS = 90
QUITAR_PRIMER_DIA_DESPUES_HORAS = 14


def get_cit_dias_disponibles(
    database: Session,
    size: int = 100,
) -> List[date]:
    """Consultar los dias disponibles, entrega un listado de fechas"""

    # Consultar dias inhabiles a partir de hoy
    cit_dias_inhabiles = get_cit_dias_inhabiles(database=database)
    fechas_inhabiles = [item.fecha for item in cit_dias_inhabiles.all()]

    # Crear listado con cada dia hasta el limite a partir de manana
    dias_disponibles = []
    for fecha in (date.today() + timedelta(n) for n in range(1, LIMITE_DIAS)):
        if fecha.weekday() in (5, 6):
            continue  # Quitar los sabados y domingos
        if fecha in fechas_inhabiles:
            continue  # Quitar los dias inhabiles
        dias_disponibles.append(fecha)  # Acumular

    # Determinar tiempo local
    servidor_tiempo = datetime.now(pytz.UTC)
    tiempo_local = servidor_tiempo.astimezone(pytz.timezone("America/Mexico_City"))

    # El dia de hoy
    hoy = tiempo_local.date()

    # Determinar si hoy es dia inhabil
    hoy_es_dia_inhabil = hoy.weekday() in (5, 6) or hoy in fechas_inhabiles

    # Si hoy es dia inhabil
    if hoy_es_dia_inhabil:
        dias_disponibles.pop(0)  # Quitar el primer dia disponible
    elif tiempo_local.hour >= QUITAR_PRIMER_DIA_DESPUES_HORAS:
        dias_disponibles.pop(0)  # Quitar el primer dia disponible

    # Crear listado de fechas a entregar cuyo tamanio sea size
    listado = []
    for fecha in dias_disponibles:
        listado.append(fecha)
        if len(listado) >= size:
            break

    # Entregar
    return listado


def get_cit_dia_disponible(database: Session) -> date:
    """Obtener el proximo dia disponible, por ejemplo, si hoy es viernes y el lunes es dia inhabil, entrega el martes"""
    return get_cit_dias_disponibles(database=database, size=1)[0]

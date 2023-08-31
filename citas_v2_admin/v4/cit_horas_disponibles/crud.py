"""
Cit Horas Disponibles v4, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyNotValidParamError

from ..cit_citas_anonimas.crud import get_cit_citas_anonimas
from ..cit_dias_disponibles.crud import get_cit_dias_disponibles
from ..cit_horas_bloqueadas.crud import get_cit_horas_bloqueadas
from ..cit_servicios.crud import get_cit_servicio
from ..oficinas.crud import get_oficina


def get_cit_horas_disponibles(
    database: Session,
    cit_servicio_id: int,
    fecha: date,
    oficina_id: int,
    size: int = 100,
) -> Any:
    """Consultar los horas disponibles activos"""

    # Consultar la oficina
    oficina = get_oficina(database, oficina_id)

    # Consultar el servicio
    cit_servicio = get_cit_servicio(database, cit_servicio_id)

    # Validar la fecha, debe ser un dia disponible
    if fecha not in get_cit_dias_disponibles(database):
        raise MyNotValidParamError("No es valida la fecha")

    # Tomar los tiempos de inicio y termino de la oficina
    apertura = oficina.apertura
    cierre = oficina.cierre

    # Si el servicio tiene un tiempo desde
    if cit_servicio.desde and apertura < cit_servicio.desde:
        apertura = cit_servicio.desde

    # Si el servicio tiene un tiempo hasta
    if cit_servicio.hasta and cierre > cit_servicio.hasta:
        cierre = cit_servicio.hasta

    # Definir los tiempos de inicio, de final y el timedelta de la duracion
    tiempo_inicial = datetime(
        year=fecha.year,
        month=fecha.month,
        day=fecha.day,
        hour=apertura.hour,
        minute=apertura.minute,
        second=0,
    )
    tiempo_final = datetime(
        year=fecha.year,
        month=fecha.month,
        day=fecha.day,
        hour=cierre.hour,
        minute=cierre.minute,
        second=0,
    )
    duracion = timedelta(
        hours=cit_servicio.duracion.hour,
        minutes=cit_servicio.duracion.minute,
    )

    # Consultar las horas bloqueadas
    cit_horas_bloqueadas = get_cit_horas_bloqueadas(database, fecha, oficina_id).all()

    # Convertir las horas bloqueadas a datetime
    tiempos_bloqueados = []
    for cit_hora_bloqueada in cit_horas_bloqueadas:
        tiempo_bloquedo_inicia = datetime(
            year=fecha.year,
            month=fecha.month,
            day=fecha.day,
            hour=cit_hora_bloqueada.inicio.hour,
            minute=cit_hora_bloqueada.inicio.minute,
            second=0,
        )
        tiempo_bloquedo_termina = datetime(
            year=fecha.year,
            month=fecha.month,
            day=fecha.day,
            hour=cit_hora_bloqueada.termino.hour,
            minute=cit_hora_bloqueada.termino.minute,
            second=0,
        ) - timedelta(minutes=1)
        tiempos_bloqueados.append((tiempo_bloquedo_inicia, tiempo_bloquedo_termina))

    # Acumular las citas agendadas en un diccionario de tiempos y cantidad de citas, para la oficina en la fecha
    # { 08:30: 2, 08:45: 1, 10:00: 2,... }
    citas_ya_agendadas = {}
    for cit_cita in get_cit_citas_anonimas(database, fecha, oficina_id).all():
        if cit_cita.inicio not in citas_ya_agendadas:
            citas_ya_agendadas[cit_cita.inicio] = 1
        else:
            citas_ya_agendadas[cit_cita.inicio] += 1

    # Bucle por los intervalos
    listado = []
    tiempo = tiempo_inicial
    while tiempo < tiempo_final:
        # Bandera
        es_hora_disponible = True
        # Quitar las horas bloqueadas
        for tiempo_bloqueado in tiempos_bloqueados:
            if tiempo_bloqueado[0] <= tiempo <= tiempo_bloqueado[1]:
                es_hora_disponible = False
                break
        # Quitar las horas ocupadas
        if tiempo in citas_ya_agendadas:
            if citas_ya_agendadas[tiempo] >= oficina.limite_personas:
                es_hora_disponible = False
        # Acumular si es hora disponible
        if es_hora_disponible:
            listado.append(tiempo.time())
        # Terminar bucle si se alcanza el tamaño
        if len(listado) >= size:
            break
        # Siguiente intervalo
        tiempo = tiempo + duracion

    # Entregar listado
    return listado

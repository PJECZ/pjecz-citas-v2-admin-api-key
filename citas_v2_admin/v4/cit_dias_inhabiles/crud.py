"""
Cit Dias Inhabiles v4, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError

from ...core.cit_dias_inhabiles.models import CitDiaInhabil


def get_cit_dias_inhabiles(
    database: Session,
    fecha_desde: date = None,
    fecha_hasta: date = None,
) -> Any:
    """Consultar los dias inhabiles activos"""
    consulta = database.query(CitDiaInhabil)
    if fecha_desde is not None:
        consulta = consulta.filter(CitDiaInhabil.fecha >= fecha_desde)
    if fecha_hasta is not None:
        consulta = consulta.filter(CitDiaInhabil.fecha <= fecha_hasta)
    return consulta.filter(CitDiaInhabil.estatus == "A").order_by(CitDiaInhabil.fecha)


def get_cit_dia_inhabil(database: Session, cit_dia_inhabil_id: int) -> CitDiaInhabil:
    """Consultar un dia inhabil por su id"""
    cit_dia_inhabil = database.query(CitDiaInhabil).get(cit_dia_inhabil_id)
    if cit_dia_inhabil is None:
        raise MyNotExistsError("No existe ese dia inhabil")
    if cit_dia_inhabil.estatus != "A":
        raise MyIsDeletedError("No es activo ese dia inhabil, está eliminado")
    return cit_dia_inhabil


def get_cit_dia_inhabil_with_fecha(database: Session, fecha: date) -> CitDiaInhabil:
    """Consultar un dia inhabil por su fecha"""
    cit_dia_inhabil = database.query(CitDiaInhabil).filter_by(fecha=fecha).first()
    if cit_dia_inhabil is None:
        raise MyNotExistsError("No existe ese dia inhabil")
    if cit_dia_inhabil.estatus != "A":
        raise MyIsDeletedError("No es activo ese dia inhabil, está eliminado")
    return cit_dia_inhabil


def create_cit_dia_inhabil(database: Session, cit_dia_inhabil: CitDiaInhabil) -> CitDiaInhabil:
    """Crear un dia inhabil"""
    database.add(cit_dia_inhabil)
    database.commit()
    database.refresh(cit_dia_inhabil)
    return cit_dia_inhabil


def update_cit_dia_inhabil(database: Session, cit_dia_inhabil_id: int, cit_dia_inhabil_in: CitDiaInhabil) -> CitDiaInhabil:
    """Actualizar un dia inhabil"""
    cit_dia_inhabil = get_cit_dia_inhabil(database, cit_dia_inhabil_id)
    cit_dia_inhabil.columna = cit_dia_inhabil_in.columna
    cit_dia_inhabil.columna = cit_dia_inhabil_in.columna
    database.commit()
    return cit_dia_inhabil


def delete_cit_dia_inhabil(database: Session, cit_dia_inhabil_id: int) -> CitDiaInhabil:
    """Eliminar un dia inhabil"""
    cit_dia_inhabil = get_cit_dia_inhabil(database, cit_dia_inhabil_id)
    cit_dia_inhabil.estatus = "B"
    database.commit()
    return cit_dia_inhabil

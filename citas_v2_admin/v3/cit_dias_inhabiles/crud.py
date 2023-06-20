"""
Citas Dias Inhabiles v3, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyAlreadyExistsError

from ...core.cit_dias_inhabiles.models import CitDiaInhabil


def get_cit_dias_inhabiles(
    db: Session,
    fecha_desde: date = None,
    fecha_hasta: date = None,
) -> Any:
    """Consultar los dias inhabiles activos"""
    consulta = db.query(CitDiaInhabil)
    if fecha_desde is not None:
        consulta = consulta.filter(CitDiaInhabil.fecha >= fecha_desde)
    if fecha_hasta is not None:
        consulta = consulta.filter(CitDiaInhabil.fecha <= fecha_hasta)
    return consulta.filter_by(estatus="A").order_by(CitDiaInhabil.fecha)


def get_cit_dia_inhabil(db: Session, cit_dia_inhabil_id: int) -> CitDiaInhabil:
    """Consultar un dia inhabil por su id"""
    cit_dia_inhabil = db.query(CitDiaInhabil).get(cit_dia_inhabil_id)
    if cit_dia_inhabil is None:
        raise MyNotExistsError("No existe ese dia inhabil")
    if cit_dia_inhabil.estatus != "A":
        raise MyIsDeletedError("No es activo ese dia inhabil, está eliminado")
    return cit_dia_inhabil


def get_cit_dia_inhabil_with_fecha(db: Session, fecha: date) -> CitDiaInhabil:
    """Consultar un dia inhabil por su fecha"""
    cit_dia_inhabil = db.query(CitDiaInhabil).filter_by(fecha=fecha).first()
    if cit_dia_inhabil is None:
        raise MyNotExistsError("No existe ese dia inhabil")
    if cit_dia_inhabil.estatus != "A":
        raise MyIsDeletedError("No es activo ese dia inhabil, está eliminado")
    return cit_dia_inhabil


def create_cit_dia_inhabil(db: Session, cit_dia_inhabil: CitDiaInhabil) -> CitDiaInhabil:
    """Crear un dia inhabil"""
    try:
        get_cit_dia_inhabil_with_fecha(db, cit_dia_inhabil.fecha)
    except MyNotExistsError:
        db.add(cit_dia_inhabil)
        db.commit()
        db.refresh(cit_dia_inhabil)
        return cit_dia_inhabil
    raise MyAlreadyExistsError("Ya existe ese dia inhabil")


def update_cit_dia_inhabil(db: Session, cit_dia_inhabil_id: int, cit_dia_inhabil_in: CitDiaInhabil) -> CitDiaInhabil:
    """Actualizar un dia inhabil"""
    cit_dia_inhabil = get_cit_dia_inhabil(db, cit_dia_inhabil_id)
    cit_dia_inhabil.columna = cit_dia_inhabil_in.columna
    cit_dia_inhabil.columna = cit_dia_inhabil_in.columna
    db.commit()
    return cit_dia_inhabil


def delete_cit_dia_inhabil(db: Session, cit_dia_inhabil_id: int) -> CitDiaInhabil:
    """Eliminar un dia inhabil"""
    cit_dia_inhabil = get_cit_dia_inhabil(db, cit_dia_inhabil_id)
    cit_dia_inhabil.estatus = "B"
    db.commit()
    return cit_dia_inhabil

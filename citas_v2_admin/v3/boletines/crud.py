"""
Boletines v3, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_string

from ...core.boletines.models import Boletin


def get_boletines(
    db: Session,
    estado: str = None,
    envio_programado_desde: date = None,
    envio_programado_hasta: date = None,
) -> Any:
    """Consultar los boletines activos"""
    consulta = db.query(Boletin)
    if estado is not None:
        estado = safe_string(estado)
        if estado in Boletin.ESTADOS:
            consulta = consulta.filter_by(estado=estado)
        else:
            raise MyNotValidParamError("No es un estado válido")
    if envio_programado_desde is not None:
        consulta = consulta.filter(Boletin.envio_programado >= envio_programado_desde)
    if envio_programado_hasta is not None:
        consulta = consulta.filter(Boletin.envio_programado <= envio_programado_hasta)
    return consulta.filter_by(estatus="A").order_by(Boletin.envio_programado)


def get_boletin(db: Session, boletin_id: int) -> Boletin:
    """Consultar un boletin por su id"""
    boletin = db.query(Boletin).get(boletin_id)
    if boletin is None:
        raise MyNotExistsError("No existe ese boletin")
    if boletin.estatus != "A":
        raise MyIsDeletedError("No es activo ese boletin, está eliminado")
    return boletin


def create_boletin(db: Session, boletin: Boletin) -> Boletin:
    """Crear un boletin"""
    db.add(boletin)
    db.commit()
    db.refresh(boletin)
    return boletin


def update_boletin(db: Session, boletin_id: int, boletin_in: Boletin) -> Boletin:
    """Actualizar un boletin"""
    boletin = get_boletin(db, boletin_id)
    boletin.asunto = boletin_in.asunto
    boletin.contenido = boletin_in.contenido
    boletin.estado = boletin_in.estado
    boletin.envio_programado = boletin_in.envio_programado
    boletin.puntero = boletin_in.puntero
    boletin.termino_programado = boletin_in.termino_programado
    db.commit()
    db.refresh(boletin)
    return boletin


def delete_boletin(db: Session, boletin_id: int) -> Boletin:
    """Eliminar un boletin"""
    boletin = get_boletin(db, boletin_id)
    boletin.estatus = "B"
    db.commit()
    db.refresh(boletin)
    return boletin

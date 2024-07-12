"""
Oficinas v4, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError, MyNotValidParamError
from lib.safe_string import safe_clave

from ...core.oficinas.models import Oficina
from ..distritos.crud import get_distrito, get_distrito_with_clave
from ..domicilios.crud import get_domicilio


def get_oficinas(
    database: Session,
    distrito_id: int = None,
    distrito_clave: str = None,
    domicilio_id: int = None,
    es_jurisdiccional: bool = None,
    puede_agendar_citas: bool = None,
    puede_enviar_qr: bool = None,
) -> Any:
    """Consultar las oficinas activas"""
    consulta = database.query(Oficina)
    if distrito_id is not None:
        distrito = get_distrito(database, distrito_id)
        consulta = consulta.filter_by(distrito_id=distrito.id)
    elif distrito_clave is not None:
        distrito = get_distrito_with_clave(database, distrito_clave)
        consulta = consulta.filter_by(distrito_id=distrito.id)
    if domicilio_id is not None:
        domicilio = get_domicilio(database, domicilio_id)
        consulta = consulta.filter(Oficina.domicilio == domicilio)
    if es_jurisdiccional is not None:
        consulta = consulta.filter_by(es_jurisdiccional=es_jurisdiccional)
    if puede_agendar_citas is not None:
        consulta = consulta.filter_by(puede_agendar_citas=puede_agendar_citas)
    if puede_enviar_qr is not None:
        consulta = consulta.filter_by(puede_enviar_qr=puede_enviar_qr)
    return consulta.filter(Oficina.estatus == "A").order_by(Oficina.clave)


def get_oficina(database: Session, oficina_id: int) -> Oficina:
    """Consultar una oficina por su id"""
    oficina = database.query(Oficina).get(oficina_id)
    if oficina is None:
        raise MyNotExistsError("No existe ese oficina")
    if oficina.estatus != "A":
        raise MyIsDeletedError("No es activo ese oficina, está eliminado")
    return oficina


def get_oficina_with_clave(database: Session, oficina_clave: str) -> Oficina:
    """Consultar una oficina por su clave"""
    try:
        clave = safe_clave(oficina_clave)
    except ValueError as error:
        raise MyNotValidParamError(str(error)) from error
    oficina = database.query(Oficina).filter_by(clave=clave).first()
    if oficina is None:
        raise MyNotExistsError("No existe ese oficina")
    if oficina.estatus != "A":
        raise MyIsDeletedError("No es activo ese oficina, está eliminado")
    return oficina

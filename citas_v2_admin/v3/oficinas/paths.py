"""
Oficinas v3, rutas (paths)
"""
from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import DatabaseSession
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import CurrentUser

from .crud import get_oficinas, get_oficina_with_clave
from .schemas import OficinaOut, OneOficinaOut

oficinas = APIRouter(prefix="/v3/oficinas", tags=["oficinas"])


@oficinas.get("", response_model=CustomPage[OficinaOut])
async def listado_oficinas(
    current_user: CurrentUser,
    db: DatabaseSession,
    distrito_id: int = None,
    distrito_clave: str = None,
    domicilio_id: int = None,
    es_jurisdiccional: bool = None,
    puede_agendar_citas: bool = None,
    puede_enviar_qr: bool = None,
):
    """Listado de oficinas"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_oficinas(
            db=db,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            domicilio_id=domicilio_id,
            es_jurisdiccional=es_jurisdiccional,
            puede_agendar_citas=puede_agendar_citas,
            puede_enviar_qr=puede_enviar_qr,
        )
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@oficinas.get("/{oficina_clave}", response_model=OneOficinaOut)
async def detalle_oficina(
    current_user: CurrentUser,
    db: DatabaseSession,
    oficina_clave: str,
):
    """Detalle de una oficina a partir de su clave"""
    if current_user.permissions.get("OFICINAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        oficina = get_oficina_with_clave(db, oficina_clave)
    except MyAnyError as error:
        return OneOficinaOut(success=False, message=str(error))
    return OneOficinaOut.from_orm(oficina)

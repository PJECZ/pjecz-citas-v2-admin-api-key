"""
Autoridades v3, rutas (paths)
"""
from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import DatabaseSession
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import CurrentUser

from .crud import get_autoridades, get_autoridad_with_clave
from .schemas import AutoridadOut, OneAutoridadOut

autoridades = APIRouter(prefix="/v3/autoridades", tags=["autoridades"])


@autoridades.get("", response_model=CustomPage[AutoridadOut])
async def listado_autoridades(
    current_user: CurrentUser,
    db: DatabaseSession,
    distrito_id: int = None,
    distrito_clave: str = None,
    es_jurisdiccional: bool = None,
    es_notaria: bool = None,
    es_organo_especializado: bool = None,
    materia_id: int = None,
    materia_clave: str = None,
):
    """Listado de autoridades"""
    if current_user.permissions.get("AUTORIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_autoridades(
            db=db,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            es_jurisdiccional=es_jurisdiccional,
            es_notaria=es_notaria,
            es_organo_especializado=es_organo_especializado,
            materia_id=materia_id,
            materia_clave=materia_clave,
        )
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@autoridades.get("/{autoridad_clave}", response_model=OneAutoridadOut)
async def detalle_autoridad(
    current_user: CurrentUser,
    db: DatabaseSession,
    autoridad_clave: str,
):
    """Detalle de una autoridad a partir de su clave"""
    if current_user.permissions.get("AUTORIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        autoridad = get_autoridad_with_clave(db, autoridad_clave)
    except MyAnyError as error:
        return OneAutoridadOut(success=False, message=str(error))
    return OneAutoridadOut.from_orm(autoridad)

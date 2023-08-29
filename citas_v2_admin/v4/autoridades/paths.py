"""
Autoridades v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_autoridad_with_clave, get_autoridades
from .schemas import AutoridadOut, OneAutoridadOut

autoridades = APIRouter(prefix="/v4/autoridades", tags=["autoridades"])


@autoridades.get("", response_model=CustomPage[AutoridadOut])
async def paginado_autoridades(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    distrito_id: int = None,
    distrito_clave: str = None,
    es_jurisdiccional: bool = None,
    es_notaria: bool = None,
    es_organo_especializado: bool = None,
    materia_id: int = None,
    materia_clave: str = None,
):
    """Paginado de autoridades"""
    if current_user.permissions.get("AUTORIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_autoridades(
            database=database,
            distrito_id=distrito_id,
            distrito_clave=distrito_clave,
            es_jurisdiccional=es_jurisdiccional,
            es_notaria=es_notaria,
            es_organo_especializado=es_organo_especializado,
            materia_id=materia_id,
            materia_clave=materia_clave,
        )
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@autoridades.get("/{clave}", response_model=OneAutoridadOut)
async def detalle_autoridad(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    clave: str,
):
    """Detalle de una autoridad a partir de su clave"""
    if current_user.permissions.get("AUTORIDADES", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        autoridad = get_autoridad_with_clave(database, clave)
    except MyAnyError as error:
        return OneAutoridadOut(success=False, message=str(error))
    return OneAutoridadOut.model_validate(autoridad)

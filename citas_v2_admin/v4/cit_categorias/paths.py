"""
Cit Categorias v4, rutas (paths)
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import Session, get_db
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage

from ...core.permisos.models import Permiso
from ..usuarios.authentications import UsuarioInDB, get_current_active_user
from .crud import get_cit_categoria, get_cit_categorias
from .schemas import CitCategoriaOut, OneCitCategoriaOut

cit_categorias = APIRouter(prefix="/v4/cit_categorias", tags=["citas"])


@cit_categorias.get("", response_model=CustomPage[CitCategoriaOut])
async def paginado_cit_categorias(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
):
    """Paginado de categorias"""
    if current_user.permissions.get("CIT CATEGORIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_categorias(database)
    except MyAnyError as error:
        return CustomPage(success=False, message=str(error))
    return paginate(resultados)


@cit_categorias.get("/{cit_categoria_id}", response_model=OneCitCategoriaOut)
async def detalle_cit_categoria(
    current_user: Annotated[UsuarioInDB, Depends(get_current_active_user)],
    database: Annotated[Session, Depends(get_db)],
    cit_categoria: int,
):
    """Detalle de una categoria a partir de su id"""
    if current_user.permissions.get("CIT CATEGORIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_categoria = get_cit_categoria(database, cit_categoria)
    except MyAnyError as error:
        return OneCitCategoriaOut(success=False, message=str(error))
    return OneCitCategoriaOut.model_validate(cit_categoria)

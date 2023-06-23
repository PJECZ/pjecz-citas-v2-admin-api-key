"""
Cit Categorias v3, rutas (paths)
"""
from fastapi import APIRouter, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate

from lib.database import DatabaseSession
from lib.exceptions import MyAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from ...core.permisos.models import Permiso
from ..usuarios.authentications import CurrentUser

from .crud import get_cit_categorias, get_cit_categoria
from .schemas import CitCategoriaOut, OneCitCategoriaOut

cit_categorias = APIRouter(prefix="/v3/cit_categorias", tags=["citas"])


@cit_categorias.get("", response_model=CustomPage[CitCategoriaOut])
async def listado_cit_categorias(
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """Listado de cetagorias"""
    if current_user.permissions.get("CIT CATEGORIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        resultados = get_cit_categorias(db)
    except MyAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@cit_categorias.get("/{cit_categoria_id}", response_model=OneCitCategoriaOut)
async def detalle_cit_categoria(
    current_user: CurrentUser,
    db: DatabaseSession,
    cit_categoria_id: int,
):
    """Detalle de una categoria a partir de su id"""
    if current_user.permissions.get("CIT CATEGORIAS", 0) < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_categoria = get_cit_categoria(db, cit_categoria_id)
    except MyAnyError as error:
        return OneCitCategoriaOut(success=False, message=str(error))
    return OneCitCategoriaOut.from_orm(cit_categoria)

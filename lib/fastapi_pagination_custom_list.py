"""
FastAPI Pagination Custom List
"""
from typing import Generic, List, Sequence, TypeVar

from fastapi import Query
from fastapi_pagination.bases import AbstractPage, AbstractParams
from fastapi_pagination.default import Params as BaseParams
from pydantic.generics import GenericModel

T = TypeVar("T")


class ListParams(BaseParams):
    """Change default limit and offset"""

    size: int = Query(100, ge=1, le=400, description="Page size")


class ListResult(GenericModel, Generic[T]):
    """Result class with items, total, limit and offset"""

    total: int
    items: List[T]
    size: int


class CustomList(AbstractPage[T], Generic[T]):
    """Custom list with success and message"""

    success: bool = True
    message: str = "Success"
    result: ListResult[T]

    __params_type__ = ListParams

    @classmethod
    def create(cls, items: Sequence[T], total: int, params: AbstractParams):
        """Create"""

        if not isinstance(params, cls.__params_type__):
            raise TypeError(f"Params must be {cls.__params_type__}")

        # If total is zero, set message to "No se encontraron resultados"
        if total == 0:
            return cls(
                success=False,
                message="No se encontraron resultados",
                result=ListResult(
                    total=total,
                    items=[],
                    size=params.size,
                ),
            )

        return cls(
            result=ListResult(
                total=total,
                items=items,
                size=params.size,
            )
        )


def custom_list_success_false(error: Exception) -> CustomList:
    """Return a CustomList with success=False and message=error"""

    result = ListResult(total=0, items=[], size=0)
    return CustomList(success=False, message=str(error), result=result)

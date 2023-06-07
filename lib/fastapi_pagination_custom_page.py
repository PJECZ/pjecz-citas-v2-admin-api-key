"""
FastAPI Pagination Custom Page

Provides a custom pagination class to be used with FastAPI.

This is an example of the output JSON:

    {
        "success": true,
        "message": "Success",
        "result": {
            "total": 13613,
            "items": [
                { ... },
                { ... },
                ...
            ],
            "limit": 10,
            "offset": 0,
        }
    }

"""
from typing import Generic, List, Sequence, TypeVar

from fastapi import Query
from fastapi_pagination.bases import AbstractPage, AbstractParams
from fastapi_pagination.limit_offset import LimitOffsetParams as BaseLimitOffsetParams
from pydantic.generics import GenericModel

T = TypeVar("T")


class LimitOffsetParams(BaseLimitOffsetParams):
    """Change default limit and offset"""

    limit: int = Query(10, ge=1, le=400, description="Query limit")
    offset: int = Query(0, ge=0, description="Query offset")


class PageResult(GenericModel, Generic[T]):
    """Result class with items, total, limit and offset"""

    total: int
    items: List[T]
    limit: int
    offset: int


class CustomPage(AbstractPage[T], Generic[T]):
    """Custom page with success and message"""

    __params_type__ = LimitOffsetParams

    success: bool = True
    message: str = "Success"
    result: PageResult[T]

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
                result=PageResult(
                    total=total,
                    items=[],
                    limit=params.limit,
                    offset=params.offset,
                ),
            )

        return cls(
            result=PageResult(
                total=total,
                items=items,
                limit=params.limit,
                offset=params.offset,
            )
        )


def custom_page_success_false(error: Exception) -> CustomPage:
    """Return a CustomPage with success=False and message=error"""

    result = PageResult(total=0, items=[], limit=0, offset=0)
    return CustomPage(success=False, message=str(error), result=result)

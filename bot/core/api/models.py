from typing import TypeVar, Optional, List, Any

from pydantic import BaseModel
from pydantic_core import PydanticUndefined

T = TypeVar('T', bound=BaseModel)

# There is cases when 'None' can be an expected value,
# so default of optional parameters must be set as '_Unset', so they will be ignored.
_Unset: Any = PydanticUndefined


class PageQuery(BaseModel):
    page: Optional[int] = 1


class RetrieveQuery(BaseModel):
    pk: int


class PaginatedRetrieveQuery(PageQuery, RetrieveQuery):
    pass


class PaginatedResult[T](BaseModel):
    count: int
    max_pages: int
    next: Optional[int] = None
    previous: Optional[int] = None
    results: List[T]

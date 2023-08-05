from typing import List
from typing import TypedDict

from testlodge._types import DateTimeStr
from testlodge._types import Pagination


class SuiteSectionJSON(TypedDict):

    id: int
    title: str
    suite_id: int
    created_at: DateTimeStr
    updated_at: DateTimeStr


class SuiteSectionListJSON(TypedDict):

    pagination: Pagination
    suite_sections: List[SuiteSectionJSON]

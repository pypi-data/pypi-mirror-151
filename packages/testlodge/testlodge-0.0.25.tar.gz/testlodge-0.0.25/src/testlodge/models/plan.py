from typing import List
from typing import TypedDict

from testlodge._types import DateTimeStr
from testlodge._types import Pagination


class PlanJSON(TypedDict):

    id: int
    name: str
    test_plan_identifier: str
    project_id: int
    created_at: DateTimeStr
    updated_at: DateTimeStr


class PlanListJSON(TypedDict):

    pagination: Pagination
    steps: List[PlanJSON]

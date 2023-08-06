from typing import List
from typing import TypedDict

from testlodge._types import DateTimeStr
from testlodge._types import Pagination


class UserJSON(TypedDict):

    id: int
    firstname: str
    lastname: str
    email: str
    created_at: DateTimeStr
    updated_at: DateTimeStr


class UserListJSON(TypedDict):

    pagination: Pagination
    users: List[UserJSON]

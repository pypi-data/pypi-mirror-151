from enum import auto
from enum import IntEnum


class SortOrder(IntEnum):
    """Method to sort by."""

    CREATED_AT = auto()
    UPDATED_AT = auto()
    NAME = auto()

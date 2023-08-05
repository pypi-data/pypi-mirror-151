from typing import Optional
from typing import TypedDict
from typing import Union


Identifier = Union[str, int]
DateTimeStr = str  # Type Alias

Pagination = TypedDict(
    'Pagination',
    {
        'total_entries': int,
        'total_pages': int,
        'current_page': int,
        'next_page': Optional[int],
        'previous_page': Optional[int],
        'per_page': int,
    },
)

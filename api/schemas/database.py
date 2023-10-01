from enum import Enum


class SortOptions(int, Enum):
    """Database sort options definition."""

    ASCENDING = 1
    DESCENDING = -1

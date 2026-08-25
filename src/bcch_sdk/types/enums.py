from enum import StrEnum


class Frequency(StrEnum):
    """Frequency of a recurring event."""

    DAILY = "DAILY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    ANNUAL = "ANNUAL"


class FunctionAPI(StrEnum):
    GET_SERIES = "GetSeries"
    SEARCH_SERIES = "SearchSeries"

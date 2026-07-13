from typing import NotRequired

from src.types.auth import QueryCredentials

from src.types.enums import FunctionAPI, Frequency


class GetSeriesParams(QueryCredentials):
    timeseries: str
    firstdate: NotRequired[str]
    lastdate: NotRequired[str]
    function: FunctionAPI


class SearchSeriesParams(QueryCredentials):
    frequency: Frequency
    function: FunctionAPI

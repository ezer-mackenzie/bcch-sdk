from datetime import datetime, date

from ..exceptions import (
    InvalidDateException,
    InvalidSeriesException,
)
from ..types.auth import InternalCredentials
from ..types.enums import Frequency, FunctionAPI
from ..types.parameters import GetSeriesParams, SearchSeriesParams

from ..mappers.credentials import CredentialsMapper

from .date import DateBuilder


class ParameterBuilder:
    @classmethod
    def build_get_series_params(
        cls,
        credentials: InternalCredentials,
        time_series: str,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
    ) -> GetSeriesParams:
        normalized_series = time_series.strip()
        if not normalized_series:
            raise InvalidSeriesException("A non-empty series identifier is required.")

        query_credentials = CredentialsMapper.to_query_credentials(credentials)
        params: GetSeriesParams = {
            "user": query_credentials["user"],
            "pass": query_credentials["pass"],
            "timeseries": normalized_series,
            "function": FunctionAPI.GET_SERIES,
        }

        normalized_first_date: str | None = None
        normalized_last_date: str | None = None
        if first_date is not None:
            normalized_first_date = DateBuilder.to_string_date(first_date)
            params["firstdate"] = normalized_first_date

        if last_date is not None:
            normalized_last_date = DateBuilder.to_string_date(last_date)
            params["lastdate"] = normalized_last_date

        if (
            normalized_first_date
            and normalized_last_date
            and normalized_first_date > normalized_last_date
        ):
            raise InvalidDateException("The first date cannot be after the last date.")

        return params

    @staticmethod
    def build_search_params(
        credentials: InternalCredentials,
        frequency: Frequency,
    ) -> SearchSeriesParams:
        """Build the parameters for the API request."""

        return SearchSeriesParams(
            **CredentialsMapper.to_query_credentials(credentials),
            frequency=frequency,
            function=FunctionAPI.SEARCH_SERIES,
        )

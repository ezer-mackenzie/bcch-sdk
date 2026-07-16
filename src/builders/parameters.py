from datetime import datetime, date

from ..types.auth import InternalCredentials
from ..types.enums import Frequency, FunctionAPI
from ..types.parameters import GetSeriesParams, SearchSeriesParams

from ..mappers.credentials import CredentialsMapper

from ..builders.date import DateBuilder


class ParameterBuilder:
    @classmethod
    def build_get_series_params(
        cls,
        credentials: InternalCredentials,
        time_series: str,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
    ) -> GetSeriesParams:
        params: GetSeriesParams = {
            **CredentialsMapper.to_query_credentials(credentials),
            "timeseries": time_series,
            "function": FunctionAPI.GET_SERIES,
        }

        if first_date:
            params["firstdate"] = DateBuilder.to_string_date(first_date)

        if last_date:
            params["lastdate"] = DateBuilder.to_string_date(last_date)

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

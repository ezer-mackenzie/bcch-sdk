from datetime import date
from typing import Literal, overload

import polars
import pandas

from ..exceptions import ResponseParseException
from ..models.web_service import WebServiceResponse
from ..types.enums import Frequency

class DataFrameMapper:
    @overload
    @classmethod
    def get_series(
        cls,
        response: WebServiceResponse,
        *,
        polars_response: Literal[True] = True,
    ) -> polars.DataFrame: ...

    @overload
    @classmethod
    def get_series(
        cls,
        response: WebServiceResponse,
        *,
        polars_response: Literal[False],
    ) -> pandas.DataFrame: ...

    @classmethod
    def get_series(
        cls,
        response: WebServiceResponse,
        *,
        polars_response: bool = True,
    ) -> polars.DataFrame | pandas.DataFrame:
        if response.series is None:
            raise ResponseParseException(
                "The response did not include series data for the requested series."
            )

        if not response.series.observations:
            raise ResponseParseException(
                "The response did not contain any observations for the requested series."
            )

        series = response.series

        dates = [obs.index_date for obs in series.observations]
        values = [obs.value for obs in series.observations]

        if polars_response:
            return polars.DataFrame(
                {
                    "date": dates,
                    series.id: values,
                }
            )
        return pandas.DataFrame(
            {
                "date": dates,
                series.id: values,
            }
        )

    @overload
    @classmethod
    def search_series(
        cls,
        response: WebServiceResponse,
        *,
        polars_response: Literal[True] = True,
    ) -> polars.DataFrame: ...

    @overload
    @classmethod
    def search_series(
        cls,
        response: WebServiceResponse,
        *,
        polars_response: Literal[False],
    ) -> pandas.DataFrame: ...

    @classmethod
    def search_series(
        cls,
        response: WebServiceResponse,
        *,
        polars_response: bool = True,
    ) -> polars.DataFrame | pandas.DataFrame:
        if response.series_information is None:
            raise ResponseParseException(
                "The response did not include series information for the search request."
            )

        if len(response.series_information) == 0:
            raise ResponseParseException(
                "The response did not contain any series information."
            )

        information = response.series_information
        columns: dict[str, list[str] | list[Frequency] | list[date]] = {
            "id": [info.id for info in information],
            "frequency": [info.frequency for info in information],
            "spanish_title": [info.spanish_title for info in information],
            "english_title": [info.english_title for info in information],
            "first_observation": [info.first_observation for info in information],
            "last_observation": [info.last_observation for info in information],
            "updated_at": [info.updated_at for info in information],
            "created_at": [info.created_at for info in information],
        }

        if polars_response:
            return polars.DataFrame(columns)

        return pandas.DataFrame(columns)

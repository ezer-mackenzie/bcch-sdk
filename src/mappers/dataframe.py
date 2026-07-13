from typing import Literal
from typing import overload

import polars
import pandas

from src.exceptions import ResponseParseException
from src.models.web_service import WebServiceResponse

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

        rows = [info.model_dump() for info in response.series_information]
        
        if polars_response:
            return polars.DataFrame(rows)
        
        return pandas.DataFrame(rows)

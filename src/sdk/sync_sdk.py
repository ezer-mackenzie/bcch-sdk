import logging
from typing import Callable, overload
from typing import Literal, Sequence

from datetime import date, datetime

from dataclasses import dataclass

import polars
import pandas

from src.builders.time_series import TimeSeriesBuilder

from src.mappers.dataframe import DataFrameMapper

from src.clients.sync_client import BCChSyncClient
from src.models.web_service import WebServiceResponse
from src.concurrency import run_in_threads

from src.types.enums import Frequency

from src.exceptions import (
    InvalidConfigurationException,
    InvalidSeriesException,
)

from .base import BaseSyncSDK

logger = logging.getLogger(__name__)


@dataclass
class BCChSyncSDK(BaseSyncSDK):
    def client(self) -> BCChSyncClient:
        if self.configuration is None:
            raise InvalidConfigurationException(
                "SDK configuration is required to initialize the sync client."
            )

        logger.debug(
            "Creating BCChSyncClient from SDK with timeout=%s", self.configuration.timeout
        )

        return BCChSyncClient(
            credentials=self.configuration.credentials,
            timeout=self.configuration.timeout,
        )

    @overload
    def get_series(
        self,
        time_series: str | list[str] | dict[str, str] | None = None,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
        *,
        polars_response: Literal[True] = True,
    ) -> Sequence[polars.DataFrame]: ...

    @overload
    def get_series(
        self,
        time_series: str | list[str] | dict[str, str] | None = None,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
        *,
        polars_response: Literal[False],
    ) -> Sequence[pandas.DataFrame]: ...

    def get_series(
        self,
        time_series: str | list[str] | dict[str, str] | None = None,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
        *,
        polars_response: bool = True,
    ) -> Sequence[polars.DataFrame | pandas.DataFrame]:
        series: list[str] = TimeSeriesBuilder.to_list(time_series)

        logger.info("Fetching %d series", len(series))
        logger.debug("Requested series identifiers: %s", series)

        def make_task(serie: str) -> Callable[[], WebServiceResponse]:
            return lambda: client.get_series(serie, first_date, last_date)

        with self.client() as client:
            results = run_in_threads(
                [make_task(serie) for serie in series],
                max_workers=min(8, len(series)),
            )

        if len(results) == 0:
            logger.warning("No series data returned for requested series list")
            raise InvalidSeriesException(
                "No series data was returned for the requested series."
            )

        if len(results) == 0:
            raise InvalidSeriesException(
                "No series data was returned for the requested series."
            )

        if polars_response:
            return [(DataFrameMapper.get_series(r)) for r in results]

        return [(DataFrameMapper.get_series(r, polars_response=False)) for r in results]

    @overload
    def search_series(
        self,
        frequency: Frequency,
        *,
        polars_response: Literal[True] = True,
    ) -> polars.DataFrame | pandas.DataFrame:
        ...
    
    @overload    
    def search_series(
        self,
        frequency: Frequency,
        *,
        polars_response: Literal[False],
    ) -> polars.DataFrame | pandas.DataFrame:
            ...

    def search_series(
        self,
        frequency: Frequency,
        *,
        polars_response: bool = True,
    ) -> polars.DataFrame | pandas.DataFrame:
        logger.info("Searching series information for frequency %s", frequency)

        with self.client() as client:
            result = client.search_series(frequency)

        if polars_response:
            return DataFrameMapper.search_series(result)

        return DataFrameMapper.search_series(result, polars_response=False)

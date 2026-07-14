from collections.abc import Sequence

from typing import overload
from typing import Literal

from dataclasses import dataclass
from datetime import datetime, date

import polars
import pandas
import logging

from ..types.enums import Frequency

from ..exceptions import (
    InvalidConfigurationException,
    InvalidSeriesException,
)

from ..builders.time_series import TimeSeriesBuilder

from ..mappers.dataframe import DataFrameMapper

from ..clients.async_client import BCChAsyncClient
from ..concurrency import gather_async_tasks

from .base import BaseSDK

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class BCChAsyncSDK(BaseSDK[BCChAsyncClient]):
    def client(self) -> BCChAsyncClient:
        if self.configuration is None:
            raise InvalidConfigurationException(
                "SDK configuration is required to initialize the async client."
            )

        logger.debug(
            "Creating BCChAsyncClient from SDK with timeout=%s",
            self.configuration.timeout,
        )

        return BCChAsyncClient(
            credentials=self.configuration.credentials,
            timeout=self.configuration.timeout,
        )

    @overload
    async def get_series(
        self,
        time_series: str | list[str] | dict[str, str] | None = None,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
        *,
        polars_response: Literal[True] = True,
    ) -> Sequence[polars.DataFrame]: ...

    @overload
    async def get_series(
        self,
        time_series: str | list[str] | dict[str, str] | None = None,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
        *,
        polars_response: Literal[False],
    ) -> Sequence[pandas.DataFrame]: ...

    async def get_series(
        self,
        time_series: str | list[str] | dict[str, str] | None = None,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
        *,
        polars_response: bool = True,
    ) -> Sequence[polars.DataFrame | pandas.DataFrame]:
        series: list[str] = TimeSeriesBuilder.to_list(time_series)

        async with self.client() as client:
            logger.info("Fetching %d series asynchronously", len(series))
            logger.debug("Requested series identifiers: %s", series)
            results = await gather_async_tasks(
                [
                    client.get_series(
                        serie,
                        first_date,
                        last_date,
                    )
                    for serie in series
                ]
            )

        if not results:
            logger.warning("No async series data returned for requested series list")
            raise InvalidSeriesException(
                "No series data was returned for the requested series."
            )

        if polars_response:
            return [DataFrameMapper.get_series(r) for r in results]

        return [DataFrameMapper.get_series(r, polars_response=False) for r in results]

    @overload
    async def search_series(
        self,
        frequency: Frequency,
        *,
        polars_response: Literal[True] = True,
    ) -> polars.DataFrame: ...

    @overload
    async def search_series(
        self,
        frequency: Frequency,
        *,
        polars_response: Literal[False],
    ) -> pandas.DataFrame: ...

    async def search_series(
        self,
        frequency: Frequency,
        *,
        polars_response: bool = True,
    ) -> polars.DataFrame | pandas.DataFrame:
        logger.info("Searching series information asynchronously for frequency %s", frequency)

        async with self.client() as client:
            result = await client.search_series(frequency)

        if polars_response:
            return DataFrameMapper.search_series(result)

        return DataFrameMapper.search_series(result, polars_response=False)
